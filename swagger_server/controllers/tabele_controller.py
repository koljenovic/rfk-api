import connexion
import six
import os
import re

from rfkadapter import RFKAdapter

from flask import json
from connexion.exceptions import ProblemException

from swagger_server.models.dict_type import DictType  # noqa: E501
from swagger_server.models.update_type import UpdateType  # noqa: E501
from swagger_server.models.where_type import WhereType  # noqa: E501
from swagger_server import util


def table_filter_post(body, table):  # noqa: E501
    """Filtrira rezultate u skladu sa argumentima (SELECT)

    Filtrira rezultate u skladu sa datim argumentima, ima za cilj emulaciju SQL SELECT iskaza sa WHERE kauzulom. Vraća tabelarne metapodatke uz svaki zahtjev. # noqa: E501

    :param body: 
    :type body: list | bytes
    :param table: database name
    :type table: str

    :rtype: List[str]
    """
    def _resolve(condition):
        # < (lt), > (gt), <= (lte), >= (gte), == (eq), != (neq)
        # si - parcijalno uparivanje stringova bez obzira na mala i velika slova
        # s - parcijalno uparivanje stringova uz razlikovanje malih i velikih slova
        # x - uparivanje stringova korištenjem regularnih izraza (regex)
        _table = {
            'lt': lambda x: x < condition.value,
            'gt': lambda x: x > condition.value,
            'lte': lambda x: x <= condition.value,
            'gte': lambda x: x >= condition.value,
            'eq': lambda x: x == condition.value,
            'neq': lambda x: x != condition.value,
            'si': lambda x: x.lower().find(condition.value.lower()) >= 0,
            's': lambda x: x.find(condition.value) >= 0,
            'x': lambda x: re.search(condition.value, x) != None,
        }
        return (condition.column_name, _table[condition.comparator])

    if connexion.request.is_json:
        testing = 'X-TESTING' in connexion.request.headers
        _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
        if _db_path == None:
            # @TODO: validate path
            raise ProblemException(status=500, title='ERROR: RFK_HOME not set', detail='RFK_HOME environment variable has to be set to valid data directory path.')
        # @TODO: sanitize and validate table exists, else raise
        _adapter = RFKAdapter(_db_path + '/', table + '.DBF', 'R')
        conditions = [WhereType.from_dict(e) for e in body]  # noqa: E501
        where = [_resolve(c) for c in conditions]
        # @HERE:TODO: lambdas pack string value type - unpack lambda or something
        return(json.dumps(_adapter.filter(where)))
    
    return 'do some magic!'


def table_patch(body, table):  # noqa: E501
    """Ažurira zapise u skladu sa filterima (UPDATE)

    Ažurira jedan ili više zapisa u skladu sa datim filterima, emulira SQL UPDATE. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param table: database name
    :type table: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = UpdateType.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def table_post(body, table):  # noqa: E501
    """Dodaje novi zapis (INSERT)

    Dodaje novi zapis u tabelu, emulira SQL INSERT. # noqa: E501

    :param body: 
    :type body: list | bytes
    :param table: database name
    :type table: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = [DictType.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
