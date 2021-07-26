# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase

AUTH_HEADERS = {
    'X-API-RKEY': 'ggbTbze1HH9V5WHdctgcA8PKvnE1htlxWyczGHOgQHYHEpO13X',
    'X-API-WKEY': '1L7g6eq0LXil2xzoEv7CnwvglwWEu9PNgA2vgulNhAZR5HD1MM',
    'X-TESTING': 'true',
}

class TestMetaController(BaseTestCase):
    """MetaController integration test stubs"""
    def test_root_get(self):
        """Test case for root_get

        Listing dostupnih tabela
        """
        response = self.client.open(
            '/',
            method='GET',
            headers=AUTH_HEADERS)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))
        outcome = None
        try:
            outcome = json.loads(response.data)
        except:
            pass
        self.assertEqual(isinstance(outcome, list), True)
        self.assertTrue('uliz.dbf' in [e.lower() for e in outcome])

    def test_table_details_get(self):
        """Test case for table_details_get

        Izlistava metapodatke za tabelu
        """
        self.assert404(self.client.open(
            '/{table}/details'.format(table='zuli'),
            method='GET',
            headers=AUTH_HEADERS))
        response = self.client.open(
            '/{table}/details'.format(table='uliz'),
            method='GET',
            headers=AUTH_HEADERS)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))
        outcome = None
        try:
            outcome = json.loads(response.data)
        except:
            pass
        self.assertEqual(isinstance(outcome, list), True)

if __name__ == '__main__':
    import unittest
    unittest.main()
