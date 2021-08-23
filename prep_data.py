#! /usr/bin/env python3
import os
import re

from rfkadapter import RFKAdapter, HarbourError

def list_tables(testing=False):
    _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
    if _db_path == None or not os.path.isdir(_db_path):
        print('RFK_HOME environment variable has to be set to valid data directory path.')
    tables = []
    with os.scandir(_db_path) as db:
        for table in db:
            if table.is_file() and table.name.lower().endswith('.dbf'):
                tables.append(table.name)
    return tables

def make_adapter(table, mode='R', testing=False):
    _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
    if _db_path == None or not os.path.isdir(_db_path):
        print('RFK_HOME environment variable has to be set to valid data directory path.')
    return RFKAdapter(_db_path + ('/' if not _db_path[-1] == '/' else ''), table, mode)

if __name__ == '__main__':
    _adapter = None, None
    for table in list_tables():
        try:
            _adapter = make_adapter(table)
            if isinstance(_adapter, RFKAdapter):
                print('DONE:\t', table)
                _adapter._cache_headers()
        except UnicodeDecodeError as e:
            print(' ⚠️\tUnicodeDecodeError:', str(e))
        except HarbourError as e:
            print(' ⚠️\tHarbourError:', str(e))
        finally:
            if not _adapter:
                print('ERROR:\t', table)
            _adapter = None