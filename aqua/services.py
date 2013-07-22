import MySQLdb

class Service(object):
    def process_search(self, resource, search_params = None):
        resource = 'search_' + resource

        if hasattr(self, resource):
            return getattr(self, resource)(search_params)

class DbService(object):
    def __init__(self, db_params, *args, **kwargs):
        self.connection = MySQLdb.connect(**db_params)

        super(DbService, self).__init__(*args, **kwargs)

    def query_select(self, select):
        with self.connection as cursor:
            cursor.execute(str(select))

            fields = [x[0] for x in cursor.description]

            return [dict(zip(fields, x)) for x in cursor.fetchall()]