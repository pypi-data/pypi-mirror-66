import logging


def dump_iter_changes(session, criteria, workbook, download_attachments):
    for change in session.iter_changes(criteria):
        logging.info(u"dumping {}".format(change.toString()))
        dump_change(change, workbook)
        dump_change_attachments(change, workbook, download_attachments)


def get_change_type(item):
    from com.agile.api import ChangeConstants
    return item.getCell(ChangeConstants.ATT_COVER_PAGE_CHANGE_TYPE).toString()


def get_change_number(item):
    from com.agile.api import ChangeConstants
    return item.getCell(ChangeConstants.ATT_COVER_PAGE_NUMBER).toString()


def get_change_release_date(item):
    from com.agile.api import ChangeConstants
    from dateutil.parser import parse
    return parse(item.getCell(ChangeConstants.ATT_COVER_PAGE_DATE_RELEASED).toString())


def dump_change(change, workbook):
    from com.agile.api import ChangeConstants
    from tables import get_table_rows, get_table_header

    title_block = change.getTable(ChangeConstants.TABLE_COVERPAGE)
    page_two = change.getTable(ChangeConstants.TABLE_PAGETWO)
    affected_items = change.getTable(ChangeConstants.TABLE_AFFECTEDITEMS)

    worksheet, created = workbook.get_or_create_worksheet(get_change_type(change))
    if created:
        worksheet.append(get_table_header(title_block) + get_table_header(page_two))
    title_block_cells = get_table_rows(title_block)[0]
    worksheet.append(title_block_cells + get_table_rows(page_two)[0])

    worksheet, created = workbook.get_or_create_worksheet('Changes')
    if created:
        worksheet.append(get_table_header(title_block))
    worksheet.append(title_block_cells)

    worksheet, created = workbook.get_or_create_worksheet("{} (Affected Items)".format(get_change_type(change)))
    if created:
        worksheet.append(get_table_header(affected_items))
    for line in get_table_rows(affected_items):
        worksheet.append([get_change_number(change)] + line)


def dump_change_attachments(change, workbook, download_attachments):
    from com.agile.api import ChangeConstants
    from attachments import dump_attachment
    from tables import get_table_header

    attachments = change.getTable(ChangeConstants.TABLE_ATTACHMENTS)

    # prepare worksheet
    worksheet, created = workbook.get_or_create_worksheet('Change Attachments')
    if created:
        worksheet.append(["Change", "Attachment ID", "Location"] + get_table_header(attachments))

    for attachment in attachments.getTableIterator():
        dump_attachment(workbook, worksheet, [get_change_number(change)], attachment, 2, download_attachments)
