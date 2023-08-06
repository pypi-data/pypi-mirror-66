"""
Usage:
    agile [options] shell
    agile [options] print(classpath)
    agile [options] dump items <working-directory> [<number>] [--download-attachments]
    agile [options] dump changes <working-directory> [<number>] [--download-attachments]
    agile [options] dump deviations <working-directory> [<number>] [--download-attachments]
    agile [options] group    items       <working-directory>
    agile [options] explode  bom         <working-directory>
    agile [options] reverse  bom         <working-directory> [--with-flexible-items]
    agile [options] collapse bom         <working-directory>
    agile [options] check    bom         <working-directory>
    agile [options] merge    ibox        <working-directory>
    agile [options] merge    iba         <working-directory>
    agile [options] merge    smb         <working-directory>
    agile [options] extract  attachments <working-directory>

Options:
    --base-url=BASEURL     server [default: http://oad02.infinidat.com:8001/Agile]
    --criteria=CRITERIA    query criteria [default: [Title Block.Item Type] not in ('Program Parameters')]
"""

import os
import re
import sys
import docopt
import logging
import contextlib


def get_session(arguments):
    from session import Session, AgileCredentialsStore
    return Session(arguments['--base-url'], AgileCredentialsStore('.credentials').get_credentials(arguments['--base-url']))


def shell(arguments, *args, **kwargs):
    local = locals()
    local.update(globals())
    __import__("code").interact(banner="", local=local)


def dump_changes(arguments):
    from utils import ensure_directory_exists
    from workbook import Workbook
    from changes import dump_iter_changes, dump_change, dump_change_attachments
    session = get_session(arguments)
    workbook = Workbook(ensure_directory_exists(arguments['<working-directory>']))
    with contextlib.closing(session), contextlib.closing(workbook):
        if arguments['<number>']:
            change = session.get_change(arguments['<number>'])
            dump_change(change, workbook)
            dump_change_attachments(change, workbook, arguments['--download-attachments'])
        else:
            dump_iter_changes(session, None, workbook, arguments['--download-attachments'])


def dump_deviations(arguments):
    from utils import ensure_directory_exists
    from workbook import Workbook
    from changes import dump_change, dump_change_attachments
    session = get_session(arguments)
    workbook = Workbook(ensure_directory_exists(arguments['<working-directory>']))
    with contextlib.closing(session), contextlib.closing(workbook):
        if arguments['<number>']:
            change = session.get_change(arguments['<number>'])
            dump_change(change, workbook)
            dump_change_attachments(change, workbook, arguments['--download-attachments'])
        else:
            for change in session.iter_changes(None):
                if change.toString().startswith('D0'):
                    logging.info(u"dumping {}".format(change.toString()))
                    dump_change(change, workbook)
                    dump_change_attachments(change, workbook, arguments['--download-attachments'])


def dump_items(arguments):
    from utils import ensure_directory_exists
    from workbook import Workbook
    from items import dump_iter_items, dump_iter_item_revisions
    session = get_session(arguments)
    workbook = Workbook(ensure_directory_exists(arguments['<working-directory>']))
    with contextlib.closing(session), contextlib.closing(workbook):
        if arguments['<number>']:
            item = session.get_item(arguments['<number>'])
            dump_iter_item_revisions(item, workbook, arguments['--download-attachments'])
        else:
            dump_iter_items(session, arguments['--criteria'], workbook, arguments['--download-attachments'])


def expode_bom(arguments):
    from explode import get_bom_cache_from_spreadsheet, get_item_cache_from_spreadsheet, exploded_bom_inner
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])

    with contextlib.closing(workbook):
        bom_sheet, _ = workbook.get_or_create_worksheet('BOM')
        logging.info('building cache')
        bom_cache = get_bom_cache_from_spreadsheet(bom_sheet)

        item_sheet, _ = workbook.get_or_create_worksheet('Items and Revisions')
        item_cache = get_item_cache_from_spreadsheet(item_sheet)
        logging.info('cache ready')

        exploded_bom_sheet, _ = workbook.get_or_create_worksheet('Exploded BOM')
        source_lines = bom_sheet.iter_rows()
        exploded_bom_sheet.append(source_lines.next() + ['Title Block.Lifecycle Phase', 'Title Block.Rev Release Date'])
        for index, cells in enumerate(source_lines, start=1):
            hierarchy, number, rev = cells[0], cells[5], cells[8]
            if hierarchy != '1':
                continue
            if not bom_cache.get((number, rev), []):
                continue
            logging.info(u"exploding bom of {}-{}".format(number, rev))
            cells[0] = str(index)
            exploded_bom_sheet.append(cells + item_cache.get((number, rev), ['Preliminary', '']))
            exploded_bom_inner('{}.'.format(index), number, rev, bom_cache, item_cache, exploded_bom_sheet)


def check_bom(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    bom_sheet, _ = workbook.get_or_create_worksheet('Exploded BOM')
    rows = bom_sheet.iter_rowdicts(bom_sheet.getheader())
    rows.next()
    items_with_unreleased_items = set()
    unreleased_items = set()
    previous_row = {'Item Number': None}
    for row in rows:
        if any(char in row['Item Number'] for char in ['"', 'DOC']):
            continue
        if '.' not in row['Hierarchy']:
            assembly = row
        if previous_row['Item Number'] and previous_row['Item Number'] != row['Item Number'] and previous_row['Item Rev'] == 'WIP' and assembly['Item Rev'] != 'WIP':
            if 'Obsolete' in [assembly['Item Lifecycle Phase'], previous_row['Item Lifecycle Phase']]:
                continue
            items_with_unreleased_items.add(assembly['Item Number'])
            unreleased_items.add(previous_row['Item Number'])
        previous_row = row
    print('The following items are being used in BOMs of released items; they must be released with revision 0:\n' + '\n'.join(sorted(unreleased_items)))
    print('\nThe following aseembly items have WIP items in their BOM, need to update their BOM and release a new revision:\n' + '\n'.join(sorted(items_with_unreleased_items)))


def merge_ibox(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    ibox_sheet, _ = workbook.get_or_create_worksheet('IBOX')
    merged_ibox_sheet, _ = workbook.get_or_create_worksheet('IBOX (Merged)')
    items = {}
    numbers = set()
    rows = ibox_sheet.iter_rowdicts(ibox_sheet.getheader())
    rows.next()

    def _is_skybox(row):
        return row['IBOX MODEL'][2] == '3'

    columns = ["IBOX MODEL", "SSD", "SSD Capacity", "RACK AND DOOR TYPE", "D Card", "Disk", "SED / NON-SED", "PDU", "PDU Conn", "Wiring Configuration", 'FC Rate', 'SFP ETH Rate']
    for row in reversed(list(rows)):
        if row['Number'] in numbers:
            continue
        if row['Rev'][0] in ('W', ):
            continue
        numbers.add(row['Number'])
        if not row['Number'].startswith('F'):
            continue
        if re.match("F.2..-0.*", row['Number']):
            continue
        if row['Lifecycle Phase'] in ('Obsolete',):
            continue
        if row['Number'].endswith('B'):
            continue
        if not row['IBOX MODEL']:
            continue
        if not row['SSD']:
            row['SSD'] = '0'
        if not row['SSD Capacity']:
            row['SSD Capacity'] = '0TB'
        if not row['RACK AND DOOR TYPE']:
            if 'tangram blank' in row['Long Description'].lower():
                row['RACK AND DOOR TYPE'] = 'TANGRAM BLANK'
            elif 'tangram screen' in row['Long Description'].lower():
                row['RACK AND DOOR TYPE'] = 'TANGRAM SCREEN'
            else:
                row['RACK AND DOOR TYPE'] = 'APC DOOR'

        # INS-367 workarounds until we add support for the SKU generator

        if not row['FC Rate']:
            continue

        if not _is_skybox(row):
            row['SFP ETH Rate'] = '18x10Gb/s'

        if any(not row[column] for column in columns):
            # if one of the cells is empty, it means this is a new column
            # so older part numbers don't have a value for it
            # and those should be ignored
            continue
        key = '{}-{}'.format(row['Number'], row['Rev'][0])

        items[key] = ','.join([row[column] for column in columns])

    header = ["Index", "Item Number", "Field Values"]
    merged_ibox_sheet.writeheader(header)
    for index, (key, value) in list(enumerate(sorted(items.iteritems(), key=lambda item_tuple: item_tuple[0], reverse=True)))[::-1]:
        merged_ibox_sheet.append_rowdict({'Index': str(index+1).zfill(4), "Item Number": key, "Field Values": value}, header)


def split_merged_ibox_file(working_directory, keyword):
    with open(os.path.join(working_directory, 'IBOX (Merged).csv')) as src:
        with open(os.path.join(working_directory, 'IBOX (Merged, {}).csv'.format(keyword)), 'w') as dst:
            for line in src.xreadlines():
                if 'Item Number' in line or ',{}'.format(keyword) in line:
                    dst.write(line)


def merge_iba(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    ibox_sheet, _ = workbook.get_or_create_worksheet('IBA')
    merged_ibox_sheet, _ = workbook.get_or_create_worksheet('IBA (Merged)')
    items = {}
    numbers = set()
    rows = ibox_sheet.iter_rowdicts(ibox_sheet.getheader())
    rows.next()

    columns = ["iGuard MODEL", "SSD", "SSD Capacity", "RACK and DOOR TYPE", "D Card", "Disk", "SED/NON SED", "PDU", "PDU Conn", "COMM Type", "Wiring Configuration", "DDE Type"]
    for row in reversed(list(rows)):
        if row['Number'] in numbers:
            continue
        numbers.add(row['Number'])
        if not row['Number'].startswith('B'):
            continue
        if re.match("B.2..-0.*", row['Number']):
            continue
        if row['Lifecycle Phase'] in ('Obsolete',):
            continue
        if row['Rev'][0] in ('W', ):
            continue
        if not row['SSD']:
            row['SSD'] = '0'
        if not row['SSD Capacity']:
            row['SSD Capacity'] = '0TB'
        if not row['RACK and DOOR TYPE']:
            if 'tangram blank' in row['Long Description'].lower():
                row['RACK and DOOR TYPE'] = 'TANGRAM BLANK'
            elif 'tangram screen' in row['Long Description'].lower():
                row['RACK and DOOR TYPE'] = 'TANGRAM SCREEN'
            else:
                row['RACK and DOOR TYPE'] = 'APC DOOR'
        key = '{}-{}'.format(row['Number'], row['Rev'][0])
        items[key] = ','.join([row[column] for column in columns])

    header = ["Index", "Item Number", "Field Values"]
    merged_ibox_sheet.writeheader(header)
    for index, (key, value) in list(enumerate(sorted(items.iteritems(), key=lambda item_tuple: item_tuple[0], reverse=True)))[::-1]:
        merged_ibox_sheet.append_rowdict({'Index': str(index+1).zfill(4), "Item Number": key, "Field Values": value}, header)


def merge_smb(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    smb_sheet, _ = workbook.get_or_create_worksheet('SMB')
    merged_smb_sheet, _ = workbook.get_or_create_worksheet('SMB (Merged)')
    items = {}
    numbers = set()
    rows = smb_sheet.iter_rowdicts(smb_sheet.getheader())
    rows.next()

    columns = ["IBOX Model", "D Card", "PDU", "SMB Comm Type"]
    for row in reversed(list(rows)):
        if row['Number'] in numbers:
            continue
        if row['Number'].endswith('CS'):
            continue
        numbers.add(row['Number'])
        if row['Lifecycle Phase'] in ('Obsolete',):
            continue
        if row['Rev'][0] in ('W', ):
            continue
        key = '{}-{}'.format(row['Number'], row['Rev'][0])
        items[key] = ','.join([row[column] for column in columns])

    header = ["Index", "Item Number", "Field Values"]
    merged_smb_sheet.writeheader(header)
    for index, (key, value) in list(enumerate(sorted(items.iteritems(), key=lambda item_tuple: item_tuple[0], reverse=True)))[::-1]:
        merged_smb_sheet.append_rowdict({'Index': str(index+1).zfill(4), "Item Number": key, "Field Values": value}, header)


def strip_rev(rev):
    stripped_rev = rev.rstrip('123456789')
    if stripped_rev.endswith('-'):
        stripped_rev += rev[-1]
    return stripped_rev


def reverse_bom(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    full_bom = arguments['--with-flexible-items']

    parent = dict()

    with contextlib.closing(workbook):
        exploded_bom_sheet, _ = workbook.get_or_create_worksheet('Exploded BOM')
        parent_child_sheet, _ = workbook.get_or_create_worksheet('BOM (Parent Child Complete)' if full_bom else 'BOM (Parent Child)')
        combined, _ = workbook.get_or_create_worksheet('Items and Revisions - Combined')
        netsuite_bom_items = {(item['Number'], item['Rev']) for
                              item in combined.iter_rowdicts(combined.getheader()) if
                              item['NetSuite BOM'] == 'Yes' or full_bom}
        fieldnames = ['Father Number', 'Father Rev', 'Child Number', 'Child Rev', 'Child Dispaly Name', 'Child Quantity']
        parent_child_sheet.writeheader(fieldnames)
        rows = exploded_bom_sheet.iter_rowdicts(exploded_bom_sheet.getheader())
        rows.next()
        previous_parent, parent = None, None

        rowdicts = []

        for item in rows:
            if item['Hierarchy'].count('.') == 0:
                previous_parent = parent
                parent = item if item['Item Rev'] != 'WIP' else None
                if is_different_item_or_major_revision(previous_parent, parent, 'Item '):
                    if all(rowdict['Child Rev'] != 'WIP' for rowdict in rowdicts):
                        for rowdict in rowdicts:
                            parent_child_sheet.append_rowdict(rowdict, fieldnames)
                rowdicts[:] = []
            elif item['Hierarchy'].count('.') == 1 and parent:
                if item['Item Rev'] == 'WIP':
                    continue
                if (item['Item Number'], item['Item Rev']) in netsuite_bom_items:
                    rowdicts.append({'Father Number': parent['Item Number'],
                                     'Father Rev': parent['Item Rev'],
                                     'Child Number': item['Item Number'],
                                     'Child Rev': item['Item Rev'],
                                     'Child Display Name': item['Item Description'],
                                     'Child Quantity': item['Qty']})


def collapse_bom(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    parent_child_sheet, _ = workbook.get_or_create_worksheet('BOM (Parent Child)')
    collapsed_parent_child_sheet, _ = workbook.get_or_create_worksheet('Collapsed BOM (Parent Child)')
    fieldnames = parent_child_sheet.getheader()
    collapsed_parent_child_sheet.writeheader(fieldnames)

    combined, _ = workbook.get_or_create_worksheet('Items and Revisions - Combined')
    items = combined.iter_rowdicts(combined.getheader())
    items.next()

    serialized_items = set()
    for rowdict in items:
        key = u'{}-{}'.format(rowdict['Number'], rowdict['Rev'])
        if rowdict['Serial'] == 'Yes':
            serialized_items.add(key)

    rows = parent_child_sheet.iter_rowdicts(fieldnames)
    rows.next()

    child_count = dict()
    children = dict()
    for rowdict in rows:
        key = u'{}-{}'.format(rowdict['Father Number'], rowdict['Father Rev'])
        child_count[key] = child_count.get(key, 0) + 1

    rows = parent_child_sheet.iter_rowdicts(fieldnames)
    rows.next()

    for rowdict in rows:
        key = u'{}-{}'.format(rowdict['Father Number'], rowdict['Father Rev'])
        if child_count[key] == 1 and child_count.get(key, 0) <= 1:
            children[key] = rowdict

    rows = parent_child_sheet.iter_rowdicts(fieldnames)
    rows.next()

    for rowdict in rows:
        key = u'{}-{}'.format(rowdict['Child Number'], rowdict['Child Rev'])
        parent_key = u'{}-{}'.format(rowdict['Father Number'], rowdict['Father Rev'])
        item = dict(**rowdict)
        if key in children:
            item['Child Number'] = children[key]['Child Number']
            item['Child Rev'] = children[key]['Child Rev']

        key = u'{}-{}'.format(rowdict['Child Number'], rowdict['Child Rev'])
        parent_key = u'{}-{}'.format(rowdict['Father Number'], rowdict['Father Rev'])
        if key in serialized_items and parent_key not in serialized_items:
            # Serialized items cannot be part of non-serialized assembly
            continue
        collapsed_parent_child_sheet.append_rowdict(item, fieldnames)


def is_different_item_or_major_revision(previous_rowdict, rowdict, prefix=''):
    if not previous_rowdict:
        return False
    if not rowdict:
        return True
    item = u'{}-{}'.format(rowdict['{}Number'.format(prefix)], strip_rev(rowdict['{}Rev'.format(prefix)]))
    previous_item = u'{}-{}'.format(previous_rowdict['{}Number'.format(prefix)], strip_rev(previous_rowdict['{}Rev'.format(prefix)]))
    if rowdict['{}Rev'.format(prefix)] == 'WIP':
        return True
    return item != previous_item


def group_items(arguments):
    from workbook import Workbook
    fieldnames = []
    workbook = Workbook(arguments['<working-directory>'])
    previous_rowdict = None
    with contextlib.closing(workbook):
        items, _ = workbook.get_or_create_worksheet('Items and Revisions')
        rows = items.iter_rowdicts(items.getheader())
        rows.next()
        part_types = {row['Part Type'] for row in rows if row['Part Type']}
        for part_type in part_types:
            worksheet, _ = workbook.get_or_create_worksheet(part_type)
            fieldnames += [column for column in worksheet.getheader() if column not in fieldnames]
        combined, _ = workbook.get_or_create_worksheet('Items and Revisions - Combined')
        combined.writeheader(fieldnames)
        for part_type in part_types:
            worksheet, _ = workbook.get_or_create_worksheet(part_type)
            for rowdict in worksheet.iter_rowdicts():
                if is_different_item_or_major_revision(previous_rowdict, rowdict):
                    combined.append_rowdict(previous_rowdict, fieldnames)
                previous_rowdict = rowdict


def extract_attachments(arguments):
    from .attachments import fix_compressed_attachments
    fix_compressed_attachments(arguments['<working-directory>'])


def print_classpath(arguments):
    from pkg_resources import resource_filename
    print(resource_filename(__name__, "AgileAPI.jar"))


def main(argv=sys.argv[1:]):
    from .__version__ import __version__
    arguments = docopt.docopt(__doc__, argv=argv, version=__version__)
    logging.basicConfig(level=logging.INFO, datefmt='%H:%M:%S', format='%(asctime)s %(message)s')
    if arguments['shell']:
        shell(arguments)
    if arguments['print'] and arguments['classpath']:
        print_classpath(arguments)
    if arguments['dump'] and arguments['items']:
        dump_items(arguments)
    if arguments['dump'] and arguments['changes']:
        dump_changes(arguments)
    if arguments['dump'] and arguments['deviations']:
        dump_deviations(arguments)
    if arguments['explode'] and arguments['bom']:
        expode_bom(arguments)
    if arguments['reverse'] and arguments['bom']:
        reverse_bom(arguments)
    if arguments['collapse'] and arguments['bom']:
        collapse_bom(arguments)
    if arguments['check'] and arguments['bom']:
        check_bom(arguments)
    if arguments['merge'] and arguments['ibox']:
        merge_ibox(arguments)
    if arguments['merge'] and arguments['iba']:
        merge_iba(arguments)
    if arguments['merge'] and arguments['smb']:
        merge_smb(arguments)
    if arguments['group'] and arguments['items']:
        group_items(arguments)
    if arguments['extract'] and arguments['attachments']:
        extract_attachments(arguments)

if __name__ == "__main__":
    sys.exit(main())
