import connexion
import os
import re

from connexion.exceptions import ProblemException
from rfkadapter import RFKAdapter

class ControllerHelper:
    @staticmethod
    def make_adapter(table, mode='R', testing=False):
        _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
        if _db_path == None or not os.path.isdir(_db_path):
            raise ProblemException(status=500, title='ERROR: RFK_HOME not set', detail='RFK_HOME environment variable has to be set to valid data directory path.')
        table = re.sub(r'\W', '', table, flags=re.A)
        table += '.DBF'
        table = table.lower()
        tables = ControllerHelper.list_tables()
        tables_lower = [t.lower() for t in tables]
        if table.lower() not in tables_lower:
            raise ProblemException(status=404, title='ERROR: table %s does not exist' % table, detail='table does not exist or invalid name, only alphanumeric characters allowed in name, table name is case insensitive e.g. ULIZ.DBF == uliz.DBF == uliz.dbf')
        return RFKAdapter(_db_path + '/', tables[tables_lower.index(table)], mode)

    @staticmethod
    def list_tables(testing=False):
        _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
        tables = []
        with os.scandir(_db_path) as db:
            for table in db:
                if table.is_file() and table.name.lower().endswith('.dbf'):
                    if os.path.isfile(_db_path + '/' + table.name.split('.')[0] + '.json'):
                        tables.append(table.name)
        return sorted(tables)