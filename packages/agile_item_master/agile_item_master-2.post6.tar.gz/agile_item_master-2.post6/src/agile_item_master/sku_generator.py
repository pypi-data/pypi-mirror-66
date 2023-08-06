"""
Usage:
    sku-generator shell
    sku-generator generate gen2 <options-csv-file> <output-csv-file> <existing-ibox-csv>
    sku-generator guess <existing-ibox-csv> <filler-in-csv> <filler-out-csv>


Options:
"""

import sys
import docopt
import logging
import contextlib


def generate_gen2(arguments):
    import unicodecsv as csv
    from workbook import Worksheet
    from itertools import product

    origin = Worksheet(arguments['<existing-ibox-csv>'])
    origin_header = origin.getheader()
    existing = [{"{} {}".format(index, key): item[key] for index, key in enumerate(origin_header, start=1)} for item in origin.iter_rowdicts()]

    src = Worksheet(arguments['<options-csv-file>'])
    fieldnames = src.getheader()
    existing_mapping = {}
    for row in existing:
        if not row['27 SSD']:
            row['27 SSD'] = '0'
        if row['27 SSD'] == '0':
            row['28 SSD Vendor'] = ''
        if not row['29 RACK AND DOOR TYPE']:
            if 'tangram blank' in row['13 Long Description'].lower():
                row['29 RACK AND DOOR TYPE'] = 'TANGRAM BLANK'
            elif 'tangram screen' in row['13 Long Description'].lower():
                row['29 RACK AND DOOR TYPE'] = 'TANGRAM SCREEN'
            else:
                row['29 RACK AND DOOR TYPE'] = 'APC DOOR'
        existing_mapping[';'.join([row[key] for key in fieldnames])] = row

    options = {}
    for item in src.iter_rowdicts():
        for key, value in item.iteritems():
            if value:
                options.setdefault(key, list()).append(value)
    dst = Worksheet(arguments['<output-csv-file>'])
    dst_header = fieldnames + ['Existing SKU']
    dst.writeheader(dst_header)
    results = product(*(options[key] for key in fieldnames))
    for result in results:
        rowdict = dict(((fieldnames[index], result[index]) for index in range(len(fieldnames))))
        if rowdict['27 SSD'] == '0':
            rowdict['28 SSD Vendor'] = ''
        if rowdict['27 SSD'] == '0' and rowdict['28 SSD Vendor'] == 'SAMSUNG':
            continue
        if rowdict['27 SSD'] == '45' and rowdict['28 SSD Vendor'] == 'INTEL':
            continue
        if rowdict['27 SSD'] == '21' and rowdict['28 SSD Vendor'] == 'INTEL':
            rowdict['27 SSD'] = '24'
        if rowdict['26 IBOX MODEL'].endswith("80") and rowdict['39 SED / NON-SED'] == 'NON SED':
            continue
        if rowdict['26 IBOX MODEL'].endswith("12") and rowdict['39 SED / NON-SED'] == 'NON SED':
            continue
        existing_item = existing_mapping.get(';'.join([rowdict[key] for key in fieldnames]))
        if existing_item:
            rowdict['Existing SKU'] = existing_item['1 Number']
        dst.append_rowdict(rowdict, dst_header)


def guess(arguments):
    from workbook import Worksheet
    origin = Worksheet(arguments['<existing-ibox-csv>'])
    src = Worksheet(arguments['<filler-in-csv>'])
    src_header = src.getheader()
    dst = Worksheet(arguments['<filler-out-csv>'])
    dst.writeheader(src_header)
    for item in src.iter_rowdicts():
        serial = item.pop('serial_number')
        item.pop('sku')
        keys = item.keys()
        for line in origin.iter_rowdicts():
            if all([item[key].lower()==line[key].lower() for key in keys if item[key]]):
                item['sku'] = line['Number']+'-'+line['Rev'].rstrip('23456789')
        item['serial_number'] = serial
        dst.append_rowdict(item, src_header)


def shell(arguments, *args, **kwargs):
    local = locals()
    local.update(globals())
    __import__("code").interact(banner="", local=local)


def main(argv=sys.argv[1:]):
    arguments = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(level=logging.INFO, datefmt='%H:%M:%S', format='%(asctime)s %(message)s')
    if arguments['shell']:
        shell(arguments)
    if arguments['generate'] and arguments['gen2']:
        generate_gen2(arguments)
    if arguments['guess']:
        guess(arguments)

if __name__ == "__main__":
    sys.exit(main())
