import connexion
import six

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
        body = [WhereType.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
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
