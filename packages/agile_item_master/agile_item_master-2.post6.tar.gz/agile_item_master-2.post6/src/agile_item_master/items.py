import logging


def dump_iter_item_revisions(item, workbook, download_attachments):
    for rev, change in get_revisions(item).items():
        dump_single_item_revision(item, rev, change, workbook, download_attachments)


def dump_iter_items(session, criteria, workbook, download_attachments):
    for item in session.iter_items(criteria):
        dump_iter_item_revisions(item, workbook, download_attachments)


def dump_single_item_revision(item, rev, change, workbook, download_attachments):
    item.setRevision(change)
    logging.info(u"dumping {}-{}".format(item.toString(), rev or "Introductory"))
    dump_item(item, rev, workbook)
    dump_item_attachments(item, rev, workbook, download_attachments)
    dump_bom(item, rev, workbook)
    dump_manufacturers(item, rev, workbook)


def dump_item(item, rev, workbook):
    from com.agile.api import ItemConstants
    from tables import get_table_header, get_table_rowdicts
    title_block = item.getTable(ItemConstants.TABLE_TITLEBLOCK)
    page_two = item.getTable(ItemConstants.TABLE_PAGETWO)
    page_three = item.getTable(ItemConstants.TABLE_PAGETHREE)

    worksheet, created = workbook.get_or_create_worksheet(get_item_part_type(item))
    if created:
        fieldnames = get_table_header(title_block) + get_table_header(page_two) + get_table_header(page_three)
        worksheet.writeheader(fieldnames)
    else:
        fieldnames = worksheet.getheader()
    rowdict = get_table_rowdicts(title_block)[0]
    rowdict['Lifecycle Phase'] = 'Production' if rowdict['Rev Release Date'] and rowdict['Lifecycle Phase'] == 'Preliminary' else rowdict['Lifecycle Phase']
    rowdict['Rev'] = rev  # removing the change number
    rowdict.update(get_table_rowdicts(page_two)[0])
    rowdict.update(get_table_rowdicts(page_three)[0])
    worksheet.append_rowdict(rowdict, fieldnames)

    worksheet, created = workbook.get_or_create_worksheet('Items and Revisions')
    if created:
        fieldnames = get_table_header(title_block)
        worksheet.writeheader(fieldnames)
    else:
        fieldnames = worksheet.getheader()
    worksheet.append_rowdict(rowdict, fieldnames)


def dump_item_attachments(item, rev, workbook, download_attachments):
    from com.agile.api import ItemConstants
    from attachments import dump_attachment
    from tables import get_table_header
    attachments = item.getTable(ItemConstants.TABLE_ATTACHMENTS)

    worksheet, created = workbook.get_or_create_worksheet('Item Attachments')
    if created:
        worksheet.append(["Item", "Item Rev", "Attachment ID", "Location"] + get_table_header(attachments))

    prefix = [get_item_number(item), rev]
    for attachment in attachments.getTableIterator():
        dump_attachment(workbook, worksheet, prefix, attachment, 3, download_attachments)


def dump_bom(item, rev, workbook):
    from com.agile.api import ItemConstants
    from tables import get_table_rowdicts, get_table_header
    bom_rowdicts = get_table_rowdicts(item.getTable(ItemConstants.TABLE_BOM))
    if not bom_rowdicts:
        return

    worksheet, created = workbook.get_or_create_worksheet('BOM')
    if created:
        fieldnames = ['Hierarchy'] + get_table_header(item.getTable(ItemConstants.TABLE_BOM))
        worksheet.writeheader(fieldnames)
    else:
        fieldnames = worksheet.getheader()
    number = get_item_number(item)
    data = dict({'Hierarchy': '1', 'Item Number': number, 'Item Rev': rev,
                 'Item Lifecycle Phase': item.getValue("Title Block.Lifecycle Phase").toString()})
    worksheet.append_rowdict(data, fieldnames)
    for index, data in enumerate(bom_rowdicts, start=1):
        data['Item Rev'] = data['Item Rev'].split()[0] if data['Item Rev'].split()[:1] and not data['Item Rev'].split()[0].startswith('M') else 'WIP'  # BOM.Item Rev
        data['Item Lifecycle Phase'] = 'Production' if data['Item Rev'] and data['Item Lifecycle Phase'] == "Preliminary" else data['Item Lifecycle Phase']
        data['Hierarchy'] = '1.{}'.format(index)
        worksheet.append_rowdict(data, fieldnames)


def dump_manufacturers(item, rev, workbook):
    from com.agile.api import ItemConstants
    from tables import get_table_rowdicts, get_table_header
    mfg_rowdict = get_table_rowdicts(item.getTable(ItemConstants.TABLE_MANUFACTURERS))
    if not mfg_rowdict:
        return

    worksheet, created = workbook.get_or_create_worksheet('Manufacturers')
    if created:
        fieldnames = ['Item Number', 'Item Rev'] + get_table_header(item.getTable(ItemConstants.TABLE_MANUFACTURERS))
        worksheet.writeheader(fieldnames)
    else:
        fieldnames = worksheet.getheader()
    number = get_item_number(item)
    for index, data in enumerate(mfg_rowdict, start=1):
        data.update({'Item Number': number, 'Item Rev': rev})
        worksheet.append_rowdict(data, fieldnames)


def get_item_part_type(item):
    from com.agile.api import ItemConstants
    return item.getCell(ItemConstants.ATT_TITLE_BLOCK_PART_TYPE).toString()


def get_item_number(item):
    from com.agile.api import ItemConstants
    return item.getCell(ItemConstants.ATT_TITLE_BLOCK_NUMBER).toString()


def merge_mco(revisions):
    # MCOs do not change the revision
    for index, (change, rev) in sorted(enumerate(revisions), reverse=True):
        if change and rev.startswith('M'):
            revisions[index] = revisions[index][0], revisions[index+1][1]
            revisions.pop(index+1)
    return revisions


def get_revisions(item):
    from collections import OrderedDict
    revisions = merge_mco(item.getRevisions().items())
    if len(revisions) <= 1:
        return OrderedDict([('WIP', 'Introductory')])
    else:
        return OrderedDict(sorted(('WIP' if '(' in rev else rev, change) for change, rev in revisions if change and rev != 'Introductory'))
