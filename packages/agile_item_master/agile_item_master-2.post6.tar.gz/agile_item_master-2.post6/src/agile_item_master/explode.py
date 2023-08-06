def exploded_bom_inner(hierarchy, number, rev, bom_cache, item_cache, exploded_bom_sheet):
    for index, cells in enumerate(bom_cache.get((number, rev), []), start=1):
        for child_rev in [cells[7], 'WIP']:
            if (cells[4], child_rev) in item_cache:
                cells = cells[:14] + item_cache[(cells[4], child_rev)]
                exploded_bom_sheet.append(['{}{}'.format(hierarchy, index)] + cells)
                break
        else:
            first_revision = [key for key in item_cache.keys() if key[0] == cells[4]][0][1]
            cells = cells[:14] + item_cache[(cells[4], first_revision)]
            exploded_bom_sheet.append(['{}{}'.format(hierarchy, index)] + cells)


def get_bom_cache_from_spreadsheet(bom_sheet):
    cache = {}
    iterator = bom_sheet.iter_rows()
    iterator.next()
    for line in iterator:
        cells = line
        hierarchy, number, rev, rest = cells[0], cells[5], cells[8], cells[1:]
        if hierarchy == '1':
            parent = (number, rev)
        else:
            cache.setdefault(parent, list()).append(rest)
    return cache


def get_item_cache_from_spreadsheet(item_sheet):
    from collections import OrderedDict
    cache = OrderedDict()
    iterator = item_sheet.iter_rows()
    iterator.next()
    for line in iterator:
        cells = line
        number, rev, lifecycle_phase, rev_release_date = cells[0], cells[5], cells[2], cells[7]
        cache[(number, rev)] = [lifecycle_phase, rev_release_date]
    return cache
