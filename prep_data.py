#! /usr/bin/env python3
import os
import re
import csv

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

def make_adapter(table, code_page, mode='R', testing=False):
    _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
    if _db_path == None or not os.path.isdir(_db_path):
        print('RFK_HOME environment variable has to be set to valid data directory path.')
    return RFKAdapter(_db_path + ('/' if not _db_path[-1] == '/' else ''), table, code_page, mode, with_headers=False)

if __name__ == '__main__':
    _adapter, error = None, None
    for table in list_tables():
        try:
            _adapter = make_adapter(table, 'cp852')
            if isinstance(_adapter, RFKAdapter):
                _adapter._parse_headers(flush=True)
                print('DONE:\t', table)
        except UnicodeDecodeError as e:
            print(' ⚠️\tUnicodeDecodeError:', str(e))
            error = True
        except HarbourError as e:
            print(' ⚠️\tHarbourError:', str(e))
            error = True
        except csv.Error as e:
            print(' ⚠️\tcsv.Error:', str(e))
            error = True
        finally:
            if not _adapter or error:
                print('ERROR:\t', table)
            _adapter = None
            error = False