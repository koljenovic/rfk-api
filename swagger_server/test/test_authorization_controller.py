# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase
from swagger_server.models.dict_type import DictType

class TestAuthController(BaseTestCase):
    """AuthController integration test"""

    def test_read_auth_required(self):
        """Test case for read auth"""
        response = self.client.open(
            '/',
            method='GET')
        self.assert401(response, 'Read auth failure.')

    def test_write_auth_required(self):
        """Test case for write auth"""
        body = [DictType()]
        response = self.client.open(
            '/{table}'.format(table='ULIZ'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert401(response, 'Write auth failure.')

if __name__ == '__main__':
    import unittest
    unittest.main()
