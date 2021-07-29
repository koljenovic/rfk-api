#! /usr/bin/env python3
import os
import re

from rfkadapter import RFKAdapter

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
    try:
        return RFKAdapter(_db_path + '/', table, mode)
    except Exception as e:
        return e

if __name__ == '__main__':
    for table in list_tables():
        _adapter = make_adapter(table)
        if isinstance(_adapter, RFKAdapter):
            print('DONE:\t', table)
            _adapter._cache_headers()
        else:
            print('ERROR:\t', table)
            print(' ⚠️\t', _adapter)