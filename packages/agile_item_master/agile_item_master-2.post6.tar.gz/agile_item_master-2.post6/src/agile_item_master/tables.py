def get_table_header(table):
    return list([attribute.getFullName().split('.', 1)[1] for attribute in table.getAttributes()])


def get_table_rows(table):
    rows = []
    for row in table.getTableIterator():
        rows.append([cell.toString() for cell in row.getCells()])
    return rows


def get_table_rowdicts(table):
    rowdicts = []
    fieldnames = get_table_header(table)
    for row in table.getTableIterator():
        rowdicts.append({fieldnames[index]: cell.toString() for
                        index, cell in enumerate(row.getCells())})

    return rowdicts
