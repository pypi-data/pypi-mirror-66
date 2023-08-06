"""
Usage:
    workato [options] shell
    workato [options] print(classpath)
    workato [options] process change <number> [--bom-only | --without-bom] [--dry-run | --retry-requests]
    workato [options] process items <working-directory> [--part-type=TYPE | --item-number=NUMBER [--item-revision=REV]] [(--bom-only) | (--without-bom)] [--dry-run | --retry-requests]

Options:
    --base-url=BASEURL     server [default: http://oad02.infinidat.com:8001/Agile]
    --retry-requests
"""

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


def post_to_workato(uri, data, dry_run):
    import requests
    if dry_run:
        print(uri, data)
    else:
        response = requests.post("https://www.workato.com/service/infinidat/{}".format(uri),
                                 json=data, headers={'Accept-Encoding': 'deflate', 'API-TOKEN': 'XMZo+1ipTe2Gcfg89y3hLA=='})
        response.raise_for_status()


def call_workato_to_create_item(serialized, assembly, item_number, item_revision, title, page_two, page_three, dry_run, retry):
    # Number  Part Type   Lifecycle Phase Description Product Line(s) Rev
    # Rev Incorp Date Rev Release Date    Effectivity Date    Item Group(s)
    #Thumbnail   Base Model  Long Description    UOM PURCHASE TYPE   TEL-AD PN
    #HS Codes    Serial  Critical Item   Regulation Type     Net Weight (Kg)
    #Date Created    Send to following Subcontractors    ECCN Code
    #Country of Origin   Replaceable Part?   Qualified?  Alternative PNs
    #EOL Date    LTB Date    LTS Date    Obsolete Date   DIM TYPE
    #MEMORY SIZE LABEL COLOR MATERIAL    LABEL SIZE (mm) CONNECTOR TYPE
    #Part Subtype    RACK AND DOOR TYPE  MANUFACTURER NAME   CAPACITY FOR DISK
    #SSD OPTIONS SSD Qty BOX SIZE    INTERFACE RATE  NUMBER OF PORTS FAN AMPS
    #DIAMETER    CFM RELEASE DATE    APPLICABLE TO   FIRMWARE NAME
    #FIRMWARE NUMBER PHASE   CONNECTOR TYPE PDU  ABOVE/BELOW Temp max (C)
    #Altitude max (m)    Humidity (%)    Power Consumption (W)
    #Heat dissipation (btu)  VOLTAGE CABLE LENGTH    IP LEVEL    WATT
    #Weight (kg) INTERFACE TYPE  Cable Type  MNF code    COLOR
    #CABLE LENGTH (mm)   Left 1 Label  Color Left 1 Label Line 1 (To)
    #Left 1 Label Line 2 (From)   Left 1 Label Line 3 (P/N)  Left 2 Label Color
    #Left 2 Label Line 1 Left 2 Label Line 2 Right 1 Label Color Right 1
    #Label Line 1 (To)   Right 1 Label Line 2(From)  Right 1 Label Line 3(P/N)
    #SED Y / N   Temp max (C)    FORM FACTOR IBOX MODEL  SSD SSD Vendor
    #ATS TYPE    Server Options  D Card  Ser Type    Ser Mem Dimm Cap
    #Disk Options    Disk    SED / NON-SED   DISK MFG    Power Options
    #PDU PDU Conn    CPU Model   DAUGHTER CARD TYPE O/C  DIMM CAPACITY
    #NOD TYPE    HWR TYPE    Door Type   FAMILY TYPE PHANTOM Yes / No
    #NUMBER DISC SLOTS   MASS
    attributes = dict(**title)
    attributes.update(**page_two)
    attributes.update(**page_three)
    netsuite_po_keywords = ["IBOX", "IBA"]
    data = {
        "NETSUITE_PO": attributes.get("Part Type", "") in netsuite_po_keywords,
        'Inventory': attributes.get("Inventory Part", "") != "No",
        "Serialized": serialized == "Yes",
        "Assembly": assembly,
        "ItemNumber": item_number,
        "ItemRevision": item_revision,
        "ItemStatus": attributes.get("Lifecycle Phase", ""),
        "ProductFamily": attributes.get("Part Type", ""),
        "DIM_TYPE": attributes.get("DIM TYPE", ""),
        "MEMORY_SIZE": attributes.get("MEMORY SIZE", ""),
        "DISK_CAPACITY": attributes.get("CAPACITY FOR DISK", ""),
        "CONNECTOR_TYPE": attributes.get("CONNECTOR TYPE", ""),
        "INTERFACE_TYPE": attributes.get("INTERFACE TYPE", ""),
        "INTERFACE_RATE": attributes.get("INTERFACE RATE", ""),
        "NUMBER_OF_PORTS": attributes.get("NUMBER OF PORTS", ""),
        "DTR_CARD_TYPE": attributes.get("DAUGHTER CARD TYPE O/C", ""),
        "DIMM_CAPACITY": attributes.get("Dimm Cap", ""),
        "NOD_TYPE": attributes.get("NOD TYPE", ""),
        "PHASE": attributes.get("PHASE", ""),
        "IBOX_MODEL": attributes.get("IBOX MODEL", "") or attributes.get("iGuard MODEL", ""),
        "NUMBER_OF_SSD": attributes.get("SSD:", "") or attributes.get("SSD", ""),
        "SSD_VENDOR": attributes.get("SSD VENDOR:", "") or attributes.get("SSD VENDOR", ""),
        "RACK_AND_DOOR_TYPE": attributes.get("RACK and DOOR TYPE:", "") or attributes.get("RACK and DOOR TYPE", ""),
        "DTR_CARD": attributes.get("D Card:", "") or attributes.get("D Card", ""),
        "DISK": attributes.get("Disk:", "") or attributes.get("Disk", ""),
        "DISK_MANUFACTURER": attributes.get("DISK MFG", ""),
        "PDU": attributes.get("PDU:", "") or attributes.get("PDU", ""),
        "PDU_CONNECTOR": attributes.get("PDU Conn:", "") or attributes.get("PDU Conn", "") or attributes.get("CONNECTOR TYPE PDU", ""),
        "ABOVE_BELOW": attributes.get("ABOVE/BELOW:", "") or attributes.get("ABOVE/BELOW", ""),
        "AMPS": attributes.get("AMPS", ""),
        "VOLTAGE": attributes.get("VOLTAGE", ""),
        "SED": attributes.get("SED/NON SED:", "") or attributes.get("SED / NON-SED") or attributes.get("SED/NON SED"),
        "ItemDescription": attributes.get("Description", ""),
        "UOM": attributes.get("UOM", ""),
        "COUNTRY_OF_ORIGIN": attributes.get("Country of Origin", ""),
        "HS_CODES": attributes.get("HS Codes", ""),
        "NET_WEIGHT": attributes.get("Net Weight (Kg)", ""),
        "REPLACEABLE_PART": attributes.get("Replaceable Part?", ""),
        "QUALIFIED": attributes.get("Qualified?", ""),
        "ECCN_CODE": attributes.get("ECCN Code", ""),
        "ALTERNATIVE_PNS": attributes.get("Alternative PNs", ""),
        "SSD_CAPACITY": attributes.get("SSD Capacity"),
        "COMM_TYPE": attributes.get("Comm Type"),
        "WIRING_CONFIGURATION": attributes.get("Wiring Configuration", ""),
        "PDU_MAP": attributes.get("PDU MAP", ""),
        "SMB_COMM_TYPE": attributes.get("SMB Comm Type", ""),
        "EOL_DATE": attributes.get("EOL Date", ""),
        "FC_RATE": attributes.get("FC Rate", ""),
        "ETH_RATE": attributes.get("SFP ETH Rate", ""),
        "DDE_CONFIGURATION": attributes.get("DDE Type", "")
        }

    from requests.exceptions import RequestException
    from infi.pyutils.retry import retry_func_on

    retry_post_to_workato = retry_func_on(RequestException)(post_to_workato)
    func = retry_post_to_workato if retry else post_to_workato
    func("recipe/create_or_update_item", data, dry_run)


def call_workato_to_replace_bom(serialized, item_number, item_revision, bom_items, dry_run, retry):
    bom = []
    data = {
        "serialized": serialized == "Yes",
        "item": item_number,
        "revision": item_revision,
        "bom": bom
    }
    for item in bom_items:
        bom.extend([{'item': item['Item Number'],
                       'revision': (item['Item Rev'].split() or [''])[0],
                       'quantity': item['Qty']}])

    from requests.exceptions import RequestException
    from infi.pyutils.retry import retry_func_on

    retry_post_to_workato = retry_func_on(RequestException)(post_to_workato)
    func = retry_post_to_workato if retry else post_to_workato
    func("recipe/replace_bom", data, dry_run)


def is_included_in_netsuite_bom(arguments, bom_item):
    from com.agile.api import ItemConstants
    from tables import get_table_rowdicts
    from items import get_revisions
    session = get_session(arguments)
    item = session.get_item(bom_item['Item Number'])
    rev = bom_item['Item Rev']
    revisions = get_revisions(item)
    if rev and rev[0] not in ['(', ' ']:
        item.setRevision(revisions[rev.split()[0]])
        page_two = get_table_rowdicts(item.getTable(ItemConstants.TABLE_PAGETWO))[0]
        return page_two.get('NetSuite BOM', '') == 'Yes'
    return False


def collapse_netsuite_bom_items(arguments, serialized, netsuite_bom_items):
    from com.agile.api import ItemConstants
    from tables import get_table_rowdicts
    from items import get_revisions

    session = get_session(arguments)
    collapsed_netsuite_bom_items = []

    for bom_item in netsuite_bom_items:
        item = session.get_item(bom_item['Item Number'])

        rev = bom_item['Item Rev']
        revisions = get_revisions(item)
        if rev.split() and revisions[rev.split()[0]]:
            item.setRevision(revisions[rev.split()[0]])

        page_two = get_table_rowdicts(item.getTable(ItemConstants.TABLE_PAGETWO))[0]

        if page_two['Serial'] == 'Yes' and serialized != 'Yes':
            # Serialized items cannot be part of non-serialized assembly
            continue

        child_bom_items = get_table_rowdicts(item.getTable(ItemConstants.TABLE_BOM))
        netsuite_child_bom_items = [child_bom_item for child_bom_item in child_bom_items if
                                    is_included_in_netsuite_bom(arguments, bom_item)]
        collapsed_netsuite_bom_items += [bom_item]
        if len(netsuite_child_bom_items) == 1:
            collapsed_netsuite_bom_items[-1]['Item Number'] = netsuite_child_bom_items[-1]['Item Number']
            collapsed_netsuite_bom_items[-1]['Item Rev'] = netsuite_child_bom_items[-1]['Item Rev']
    return collapsed_netsuite_bom_items


def process_change(arguments):
    from com.agile.api import ChangeConstants, ItemConstants
    from tables import get_table_rowdicts
    from items import get_revisions
    from changes import get_change_release_date
    session = get_session(arguments)
    change = session.get_change(arguments['<number>'])
    affected_items = get_table_rowdicts(change.getTable(ChangeConstants.TABLE_AFFECTEDITEMS))

    for data in affected_items:
        item = session.get_item(data['Item Number'])
        item.setRevision(get_revisions(item)[data['New Rev']])

        title = get_table_rowdicts(item.getTable(ItemConstants.TABLE_TITLEBLOCK))[0]
        if title.get('Part Type') in ('Option Class', 'FIRMWARE VERSION', None):
            continue

        page_two = get_table_rowdicts(item.getTable(ItemConstants.TABLE_PAGETWO))[0]
        page_three = get_table_rowdicts(item.getTable(ItemConstants.TABLE_PAGETHREE))[0]
        bom_items = get_table_rowdicts(item.getTable(ItemConstants.TABLE_BOM))
        netsuite_bom_items = [bom_item for bom_item in bom_items if
                              is_included_in_netsuite_bom(arguments, bom_item)]
        collapsed_netsuite_bom_items = collapse_netsuite_bom_items(arguments, page_two['Serial'], netsuite_bom_items)

        if data['New Rev'] in ('', 'W'):
            continue

        if not arguments['--bom-only']:
            call_workato_to_create_item(page_two['Serial'], bool(collapsed_netsuite_bom_items),
                                   data['Item Number'], data['New Rev'],
                                   title, page_two, page_three,
                                   arguments['--dry-run'], arguments['--retry-requests'])

    for data in affected_items:
        item = session.get_item(data['Item Number'])
        item.setRevision(get_revisions(item)[data['New Rev']])
        process_change_in_bom(arguments, session, data, item)

        where_used = get_table_rowdicts(item.getTable(ItemConstants.TABLE_WHEREUSED))
        for parent_data in where_used:
            parent_item = session.get_item(parent_data['Item Number'])
            parent_data['New Rev'] = parent_item.getRevision()

            if parent_data['New Rev']:
                if get_change_release_date(item.getChange()) > get_change_release_date(change):
                    continue

            process_change_in_bom(arguments, session, parent_data, parent_item)


def process_change_in_bom(arguments, session, data, item):
    from com.agile.api import ItemConstants
    from tables import get_table_rowdicts

    title = get_table_rowdicts(item.getTable(ItemConstants.TABLE_TITLEBLOCK))[0]
    if title.get('Part Type') in ('Option Class', None):
        return

    page_two = get_table_rowdicts(item.getTable(ItemConstants.TABLE_PAGETWO))[0]
    bom_items = get_table_rowdicts(item.getTable(ItemConstants.TABLE_BOM))

    netsuite_bom_items = [bom_item for bom_item in bom_items if
                          is_included_in_netsuite_bom(arguments, bom_item)]

    collapsed_netsuite_bom_items = collapse_netsuite_bom_items(arguments, page_two['Serial'], netsuite_bom_items)

    if data['New Rev'] in ('', 'W'):
        return

    if not arguments['--without-bom'] and bool(collapsed_netsuite_bom_items):
        call_workato_to_replace_bom(page_two['Serial'], data['Item Number'], data['New Rev'], collapsed_netsuite_bom_items,
                                    arguments['--dry-run'], arguments['--retry-requests'])
    return item


def process_items(arguments):
    from workbook import Workbook
    workbook = Workbook(arguments['<working-directory>'])
    combined, _ = workbook.get_or_create_worksheet('Items and Revisions - Combined')
    bom_pairs, _ = workbook.get_or_create_worksheet('Collapsed BOM (Parent Child)')

    bom_pairs_iterator = bom_pairs.iter_rowdicts(bom_pairs.getheader())
    bom_pairs_iterator.next()
    item_numbers_with_bom = {u'{}-{}'.format(row['Father Number'], row['Father Rev']) for row in bom_pairs_iterator}

    items = combined.iter_rowdicts(combined.getheader())
    items.next()
    items = list(items)

    items_processed = []

    for item in items:
        if arguments.get('--part-type') and item['Part Type'] != arguments.get('--part-type'):
            continue
        if 'DELETED' in item['Number']:
            continue
        if arguments.get('--item-number') and item['Number'] != arguments.get('--item-number'):
            continue
        if arguments.get('--item-number') and arguments.get('--item-revision') and item['Rev'] != arguments.get('--item-revision'):
            continue
        if item['Rev'] in ('', 'W'):
            continue

        items_processed += [item]

        if not arguments['--bom-only']:
            call_workato_to_create_item(item['Serial'], u'{}-{}'.format(item['Number'], item['Rev']) in item_numbers_with_bom,
                                        item['Number'], item['Rev'],
                                        item, item, item,
                                        arguments['--dry-run'], arguments['--retry-requests'])

        if not arguments['--without-bom'] and '{}-{}'.format(item['Number'], item['Rev']) in item_numbers_with_bom:
            bom_pairs_iterator = bom_pairs.iter_rowdicts(bom_pairs.getheader())
            bom_pairs_iterator.next()
            children = []
            for bom_pair in bom_pairs_iterator:
                if (item['Number'], item['Rev']) == (bom_pair['Father Number'], bom_pair['Father Rev']):
                    children += [{'Item Number': bom_pair['Child Number'], 'Item Rev': bom_pair['Child Rev'],
                                  'Qty': bom_pair['Child Quantity']}]
            netsuite_children = [child_item for child_item in children if
                                 any(item['NetSuite BOM'] == 'Yes' for item in items if
                                     item['Number'] == child_item['Item Number'] and
                                     item['Rev'] == child_item['Item Rev'])]
            collapsed_netsuite_children = netsuite_children
            call_workato_to_replace_bom(item['Serial'], item['Number'], item['Rev'], collapsed_netsuite_children,
                                        arguments['--dry-run'], arguments['--retry-requests'])

    return 0 if items_processed else 1


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
    if arguments['process'] and arguments['change']:
        setup_http_debug()
        return process_change(arguments)
    if arguments['process'] and arguments['items']:
        setup_http_debug()
        return process_items(arguments)


def setup_http_debug():
    import requests
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


if __name__ == "__main__":
    sys.exit(main())
