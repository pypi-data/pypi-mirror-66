import logging


def write_attachment_to_cachedir(attachments_directory, attachment):
    from org.python.core.util import FileUtil
    from utils import ensure_directory_exists
    from os.path import exists, join
    cachedir = ensure_directory_exists(join(attachments_directory, '.cache'))
    cachefile = join(cachedir, attachment.getId().toString())
    if not exists(cachefile):
        logging.info(u"saving attachment {}".format(attachment.getId()))
        with open(cachefile, 'wb') as fd:
            with FileUtil.wrap(attachment.getFile(), 'rb') as source:
                fd.write(source.read())
    return cachefile


def dump_attachment(workbook, worksheet, prefix, attachment, name_index, download_attachments):
    from os.path import join, abspath, relpath, lexists
    from os import readlink, symlink, remove
    from utils import ensure_directory_exists
    cells = [cell.toString() for cell in attachment.getCells()]
    if download_attachments:
        attachments_directory = join(workbook.working_directory, 'attachments')
        cachefile = write_attachment_to_cachedir(attachments_directory, attachment)
        basedir = ensure_directory_exists(join(attachments_directory, *prefix))
        for basename in [cells[name_index], u'{}-{}'.format(attachment.getId(), cells[name_index])]:
            destfile = join(basedir, basename)
            if lexists(destfile) and abspath(cachefile) != abspath(join(basedir, readlink(destfile))):
                continue
            break
        cells[3] = basename
        worksheet.append(prefix + [attachment.getId(), relpath(destfile, attachments_directory)] + cells)
        if lexists(destfile):
            remove(destfile)
        symlink(relpath(cachefile, basedir), destfile)
    else:
        worksheet.append(prefix + [attachment.getId(), ''] + cells)


def is_zipfile(filepath):
    import zipfile
    try:
        zipfile.ZipFile(filepath).close()
        return True
    except zipfile.BadZipFile:
        return False


def fix_compressed_attachments(working_directory):
    from os.path import join, isfile
    from os import rename
    from glob import glob
    from zipfile import ZipFile
    attachments_directory = join(working_directory, 'attachments')
    cachedir = join(attachments_directory, '.cache')
    for filepath in glob(join(cachedir, '*')):
        if isfile(filepath) and is_zipfile(filepath):
            zip_file = ZipFile(filepath)
            if len(zip_file.filelist) == 1 and zip_file.filelist[0].filename.startswith('/\\'):
                print(filepath)
                inner_filepath = zip_file.extract(zip_file.filelist[0])
                zip_file.close()
                rename(inner_filepath, filepath)
            else:
                zip_file.close()
