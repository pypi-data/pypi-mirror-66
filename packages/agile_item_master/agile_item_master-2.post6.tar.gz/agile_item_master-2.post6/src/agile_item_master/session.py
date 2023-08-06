from infi.credentials_store import CLICredentialsStore


class AgileCredentialsStore(CLICredentialsStore):
    def _build_file_path(self):
        from os import path
        return path.join(path.expanduser('~'), '.infinidat', 'agile')

    def authenticate(self, key, credentials):
        if credentials is None:
            return False
        try:
            Session(key, credentials).close()
        except:
            return False
        return True


class Session(object):
    def __init__(self, base_url, credentials):
        from java.text import SimpleDateFormat
        from com.agile.api import AgileSessionFactory
        factory = AgileSessionFactory.getInstance(base_url)
        self._session = factory.createSession({AgileSessionFactory.USERNAME: credentials.get_username(),
                                         AgileSessionFactory.PASSWORD: credentials.get_password()})
        self._session.setDateFormats([SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssX"), SimpleDateFormat("yyyy-MM-dd")])

    def close(self):
        self._session.close()

    def get_item(self, number):
        from com.agile.api import ItemConstants
        return self._session.getObject(ItemConstants.CLASS_PART, number)

    def get_change(self, number):
        from com.agile.api import ChangeConstants
        return self._session.getObject(ChangeConstants.CLASS_CHANGE_BASE_CLASS, number)

    def iter_items(self, criteria=None):
        query = self.build_item_query(criteria)
        results = query.execute()
        for item in results:
            if item.getCell("Number"):
                yield self.get_item(item.getCell("Number").toString())

    def iter_changes(self, criteria=None):
        query = self.build_change_query(criteria)
        results = query.execute()
        for item in results:
            if item.getCell("Number"):
                yield self.get_change(item.getCell("Number").toString())

    def build_change_query(self, criteria):
        from com.agile.api import ChangeConstants, IQuery
        query = self._session.createObject(IQuery.OBJECT_TYPE, ChangeConstants.CLASS_CHANGE_BASE_CLASS)
        if criteria:
            query.setCaseSensitive(False)
            query.setCriteria(criteria)
        return query

    def build_item_query(self, criteria):
        from com.agile.api import ItemConstants, IQuery
        query = self._session.createObject(IQuery.OBJECT_TYPE, ItemConstants.CLASS_ITEM_BASE_CLASS)
        if criteria:
            query.setCaseSensitive(False)
            query.setCriteria(criteria)
        return query
