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
    if connexion.request.is_json:
        testing = 'X-TESTING' in connexion.request.headers
        _db_path = os.getenv('RFK_TEST_HOME') if testing else os.getenv('RFK_HOME')
        if _db_path == None:
            # @TODO: validate path
            raise ProblemException(status=500, title='ERROR: RFK_HOME not set', detail='RFK_HOME environment variable has to be set to valid data directory path.')
        # @TODO: sanitize and validate table exists, else raise
        _adapter = RFKAdapter(_db_path + '/', table + '.DBF', 'R')
        # @HERE@TODO: sanitize body
        
        _ = [WhereType.from_dict(e) for e in body]
        conditions = [c.values() for c in body]
        return _adapter.where(conditions)

    raise ProblemException(status=400, title='ERROR: request body not JSON or invalid', detail='request body has to be valid WhereType style JSON')


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
