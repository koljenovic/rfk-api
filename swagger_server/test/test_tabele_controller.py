# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.dict_type import DictType  # noqa: E501
from swagger_server.models.update_type import UpdateType  # noqa: E501
from swagger_server.models.where_type import WhereType  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTabeleController(BaseTestCase):
    """TabeleController integration test stubs"""

    def test_table_filter_post(self):
        """Test case for table_filter_post

        Filtrira rezultate u skladu sa argumentima (SELECT)
        """
        body = [
            WhereType('OBJ_ULI', 'eq', '010'),
            WhereType('DOK_ULI', 'eq', '20'),
            WhereType('SIF_ULI', 'eq', '915'),
        ]
        headers = {
            'X-API-RKEY': 'ggbTbze1HH9V5WHdctgcA8PKvnE1htlxWyczGHOgQHYHEpO13X',
            'X-API-WKEY': '1L7g6eq0LXil2xzoEv7CnwvglwWEu9PNgA2vgulNhAZR5HD1MM',
            'X-TESTING': 'true',
        }
        response = self.client.open(
            '/{table}/filter'.format(table='ULIZ'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        outcome = None
        try:
            outcome = json.loads(response.data)
        except:
            pass
        self.assertEqual(isinstance(outcome, list), True)
        self.assertEqual(outcome[0]['OBJ_ULI'], 10)
        self.assertEqual(outcome[0]['DOK_ULI'], 20)
        self.assertEqual(outcome[0]['SIF_ULI'], 915)
        body = [
            WhereType('OBJ_ULI', 'eq', '12'),
            WhereType('DOK_ULI', 'eq', '20'),
        ]
        response = self.client.open(
            '/{table}/filter'.format(table='ULIZ'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        outcome = None
        try:
            outcome = json.loads(response.data)
        except:
            pass
        self.assertEqual(isinstance(outcome, list), True)
        for record in outcome:
            self.assertEqual(record['OBJ_ULI'], 12)
            self.assertEqual(record['DOK_ULI'], 20)

    def test_table_patch(self):
        """Test case for table_patch

        Ažurira zapise u skladu sa filterima (UPDATE)
        """
        body = UpdateType()
        response = self.client.open(
            '/{table}'.format(table='table_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_table_post(self):
        """Test case for table_post

        Dodaje novi zapis (INSERT)
        """
        body = [DictType()]
        response = self.client.open(
            '/{table}'.format(table='ULIZ'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

if __name__ == '__main__':
    import unittest
    unittest.main()
