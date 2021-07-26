import connexion
import six
import os

from swagger_server import util
from .controller_helper import ControllerHelper

def root_get():  # noqa: E501
    """Listing dostupnih tabela

    Izlistava sve dostupne *.DBF tabele u data direktoriju (*bazi podataka*) # noqa: E501


    :rtype: List[str]
    """
    testing = 'X-TESTING' in connexion.request.headers
    return ControllerHelper.list_tables(testing=testing)


def table_details_get(table):  # noqa: E501
    """Izlistava metapodatke za tabelu

    Izlistava nazive svih kolona za datu tabelu. # noqa: E501

    :param table: database name
    :type table: str

    :rtype: List[str]
    """
    testing = 'X-TESTING' in connexion.request.headers
    _adapter = ControllerHelper.make_adapter(table, testing=testing)
    return [str(f) for f in _adapter.header_fields]
