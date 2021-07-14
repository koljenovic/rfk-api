import connexion
import six

from swagger_server import util


def root_get():  # noqa: E501
    """Listing dostupnih tabela

    Izlistava sve dostupne &#x60;*.DBF&#x60; *tabele* u &#x60;data&#x60; direktoriju (*bazi podataka*) # noqa: E501


    :rtype: List[str]
    """
    return 'do some magic!'


def table_details_get(table):  # noqa: E501
    """Izlistava metapodatke za tabelu

    Izlistava nazive svih kolona za datu tabelu. # noqa: E501

    :param table: database name
    :type table: str

    :rtype: List[str]
    """
    return 'do some magic!'
