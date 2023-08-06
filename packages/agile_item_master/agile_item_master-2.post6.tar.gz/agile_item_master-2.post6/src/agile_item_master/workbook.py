class Workbook(object):
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self._worksheets = {}

    def get_or_create_worksheet(self, name):
        from os.path import join
        try:
            return self._worksheets[name], False
        except KeyError:
            path = join(self.working_directory, name.replace('/', '_') + '.csv')
            self._worksheets[name] = Worksheet(path)
            return self._worksheets[name], True
        raise NotImplementedError()

    def close(self):
        for key, worksheet in self._worksheets.items():
            worksheet.close()
        self._worksheets.clear()

    def close_sheet(self, key):
        self._worksheets.pop(key).close()


class Worksheet(object):
    def __init__(self, name):
        self._fd = open(name, 'ab+')
        self._fieldnames = None

    def append(self, line):
        import unicodecsv as csv
        csv.writer(self._fd, quoting=csv.QUOTE_MINIMAL).writerow(line)

    def writeheader(self, fieldnames):
        import unicodecsv as csv
        csv.DictWriter(self._fd, fieldnames).writeheader()
        self._fieldnames = fieldnames

    def getheader(self):
        if self._fieldnames:
            return self._fieldnames
        pos = self._fd.tell()
        header = self.iter_rows().next()
        self._fd.seek(pos, 0)
        return header

    def append_rowdict(self, rowdict, fieldnames, extrasaction='ignore'):
        import unicodecsv as csv
        csv.DictWriter(self._fd, fieldnames, quoting=csv.QUOTE_MINIMAL, extrasaction=extrasaction).writerow(rowdict)

    def iter_rows(self):
        import unicodecsv as csv
        with open(self._fd.name) as fd:
            for item in csv.reader(fd):
                yield item

    def iter_rowdicts(self, fieldnames=None):
        import unicodecsv as csv
        self._fd.seek(0, 0)
        return iter(csv.DictReader(self._fd, fieldnames))

    def close(self):
        self._fd.close()

    def __repr__(self):
        return u'<Worksheet(name={!r})>'.format(self._fd.name)
