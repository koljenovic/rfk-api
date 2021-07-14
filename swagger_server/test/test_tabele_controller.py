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
        body = [WhereType()]
        response = self.client.open(
            '/{table}/filter'.format(table='table_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

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
            '/{table}'.format(table='table_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
