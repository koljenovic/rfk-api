import connexion
import six

from flask import json
from connexion.exceptions import ProblemException
from .controller_helper import ControllerHelper

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
        _adapter = ControllerHelper.make_adapter(table, testing=testing)
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
        testing = 'X-TESTING' in connexion.request.headers
        _adapter = ControllerHelper.make_adapter(table, mode='W', testing=testing)
        conditions = [c.values() for c in body['where']]
        body = UpdateType.from_dict(connexion.request.get_json())  # noqa: E501
        _adapter.update(body.what, conditions)
        return ''
        
    raise ProblemException(status=400, title='ERROR: request body not JSON or invalid', detail='request body has to be valid WhereType style JSON')


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
        testing = 'X-TESTING' in connexion.request.headers
        _adapter = ControllerHelper.make_adapter(table, mode='W', testing=testing)
        body = [DictType.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
        for record in body:
            _adapter.write(record)
        return ''

    raise ProblemException(status=400, title='ERROR: request body not JSON or invalid', detail='request body has to be valid WhereType style JSON')
