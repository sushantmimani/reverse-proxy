"""
Unit tests
"""

import unittest
from mock import patch
from utils import proxy_request
from reverse_proxy_service import APP


class MyTest(unittest.TestCase):
    """
    Unit tests
    """
    @patch('utils.requests.get')
    def test_request_response(self, mock_get):
        """
        Test request response of API call
        """
        mock_get.return_value[0].status = '200 OK'
        resp = proxy_request('http://localhost/api/v1/config?command=agencyList')
        self.assertEqual(mock_get.return_value[0].status, resp[0].status)

    @patch('config.requests.get')
    def test_config_response(self):
        """
        Test that incorrect endpoint returns an error
        """
        client = APP.test_client()
        resp = client.get('http://localhost/api/v1/abc?command=agencyList')
        self.assertEqual('404 NOT FOUND', resp.status)


if __name__ == '__main__':
    unittest.main()
