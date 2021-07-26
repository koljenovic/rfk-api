# coding: utf-8

from __future__ import absolute_import

import secrets

from flask import json
from six import BytesIO

from swagger_server.models.dict_type import DictType  # noqa: E501
from swagger_server.models.update_type import UpdateType  # noqa: E501
from swagger_server.models.where_type import WhereType  # noqa: E501
from swagger_server.test import BaseTestCase

AUTH_HEADERS = {
    'X-API-RKEY': 'ggbTbze1HH9V5WHdctgcA8PKvnE1htlxWyczGHOgQHYHEpO13X',
    'X-API-WKEY': '1L7g6eq0LXil2xzoEv7CnwvglwWEu9PNgA2vgulNhAZR5HD1MM',
    'X-TESTING': 'true',
}

class TestTabeleController(BaseTestCase):
    """TabeleController integration tests"""

    def test_table_filter_post(self):
        """Test case for table_filter_post

        Filtrira rezultate u skladu sa argumentima (SELECT)
        """
        body = [
            WhereType('OBJ_ULI', 'eq', '010'),
            WhereType('DOK_ULI', 'eq', '20'),
            WhereType('SIF_ULI', 'eq', '915'),
        ]
        response = self.client.open(
            '/{table}/filter'.format(table='ULIZ'),
            method='POST',
            headers=AUTH_HEADERS,
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
            headers=AUTH_HEADERS,
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
        randid = secrets.randbelow(10**4)
        what = { 'OBJ_ULI': 99, 'SIF_ULI': randid }
        where = [
            WhereType('SIF_ULI', 'eq', '883'),
            WhereType('DAT_ULI', 'gte', '2021-07-07'),
        ]
        body = UpdateType(what, where)
        response = self.client.open(
            '/{table}'.format(table='uliz'),
            method='PATCH',
            headers=AUTH_HEADERS,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))
        body = [
            WhereType('OBJ_ULI', 'eq', '99'),
            WhereType('DOK_ULI', 'eq', str(randid)),
        ]
        response = self.client.open(
            '/{table}/filter'.format(table='ULIZ'),
            method='POST',
            headers=AUTH_HEADERS,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))
        outcome = None
        try:
            outcome = json.loads(response.data)
        except:
            pass
        self.assertEqual(isinstance(outcome, list), True)
        for record in outcome:
            self.assertEqual(record['OBJ_ULI'], 99)
            self.assertEqual(record['DOK_ULI'], randid)

    def test_table_post(self):
        """Test case for table_post

        Dodaje novi zapis (INSERT)
        """
        generico = { 'DAI_ULI': '2021-06-14', 'DAN_ULI': 0, 'DAT_ULI': '2021-07-07', 'DOK_ULI': 20, 'KAS_ULI': 0, 'KUF_ULI': '1234', 'L0_ULI': False, 'L1_ULI': False, 'L2_ULI': False, 'L3_ULI': False, 'L4_ULI': False, 'L5_ULI': False, 'L6_ULI': False, 'L7_ULI': False, 'L8_ULI': False, 'L9_ULI': False, 'N1_ULI': 0, 'N2_ULI': 0, 'NAL_ULI': 'ADM', 'NAP_ULI': '', 'OBJ_ULI': 10, 'OTP_ULI': '225883', 'PAR_ULI': '0196552', 'PUT_ULI': '001', 'RBR_ULI': 2, 'SIF_ULI': 883, 'VAL_ULI': '2021-06-14', 'ZAD_ULI': '001' }
        body = [DictType.from_dict(generico), DictType.from_dict(generico)]
        response = self.client.open(
            '/{table}'.format(table='uliz'),
            method='POST',
            headers=AUTH_HEADERS,
            data=json.dumps(body),
            content_type='application/json')        
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

if __name__ == '__main__':
    import unittest
    unittest.main()
