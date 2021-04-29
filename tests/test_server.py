"""server test cases"""
# pylint: disable=no-self-use,attribute-defined-outside-init
import json

import unittest.mock as mock

from server import APP


class TestServer:
    """test server"""

    def setup_method(self):
        '''set up tests'''

    def test_resource_not_found(self):
        '''resource not found'''
        with APP.test_client() as client:
            response = client.get('/api/resource_not_found')
        assert response.status_code == 404

        expected = {'description': 'The requested URL was not found on the server.', 'message': 'Resource Not Found'}
        assert json.loads(response.data) == expected

    @mock.patch('service.reviews.ReviewRequestHandler.get')
    def test_uncaught_exception(self, handler):
        '''uncaught exception'''
        handler.side_effect = Exception
        with APP.test_client() as client:
            response = client.get('/api/reviews')
        assert response.status_code == 500

        expected = {'message': 'Internal Server Error'}
        assert json.loads(response.data) == expected
