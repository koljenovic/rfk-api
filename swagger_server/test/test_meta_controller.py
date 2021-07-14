# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestMetaController(BaseTestCase):
    """MetaController integration test stubs"""

    def test_root_get(self):
        """Test case for root_get

        Listing dostupnih tabela
        """
        response = self.client.open(
            '/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_table_details_get(self):
        """Test case for table_details_get

        Izlistava metapodatke za tabelu
        """
        response = self.client.open(
            '/{table}/details'.format(table='table_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
