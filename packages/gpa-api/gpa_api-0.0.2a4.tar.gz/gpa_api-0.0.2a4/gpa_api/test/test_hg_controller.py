# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from gpa_api.models.hg_fluid import HgFluid  # noqa: E501
from gpa_api.test import BaseTestCase


class TestHgController(BaseTestCase):
    """HgController integration test stubs"""

    def test_create_fluid(self):
        """Test case for create_fluid

        Create hg fluid
        """
        hg_fluid = {
  "components" : [ {
    "value" : 6.027456183070403
  }, {
    "value" : 6.027456183070403
  } ],
  "createdDate" : "2000-01-23T04:56:07.000+00:00",
  "name" : "name",
  "id" : 0
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hg/fluids',
            method='POST',
            headers=headers,
            data=json.dumps(hg_fluid),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_fluid(self):
        """Test case for get_fluid

        Get fluid
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hg/fluids/{fluid_id}'.format(fluid_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_fluids(self):
        """Test case for get_fluids

        Get hg fluids
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hg/fluids',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
