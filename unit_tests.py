"""
Unit tests
"""

import unittest
from mock import patch
from utils import proxy_request


def mocked_config_requests(**kwargs):
    """
    Mocks config endpoints
    """
    if kwargs['command'] == 'agencyList':
        return 200
    elif kwargs['command'] == 'routeList' and 'a' in kwargs.keys():
        return 200
    elif (kwargs['command'] == 'routeConfig' and 'a' in kwargs.keys()) or \
            (kwargs['command'] == 'routeConfig' and 'a' in kwargs.keys() and 'r' in kwargs.keys()):
        return 200
    return 404


def mocked_message_requests(**kwargs):
    """
    Mocks message endpoints
    """
    if (kwargs['command'] == 'messages' and 'a' in kwargs.keys()) or \
            (kwargs['command'] == 'messages' and 'a' in kwargs.keys() and 'r' in kwargs.keys()):
        return 200
    elif kwargs['command'] == 'vehicleLocations' and 'a' in kwargs.keys():
        return 200
    elif (kwargs['command'] == 'routeConfig' and 'a' in kwargs.keys()) and 't' in kwargs.keys() or \
            (kwargs['command'] == 'routeConfig' and 'a' in kwargs.keys() and 'r' in kwargs.keys() \
                     and 't' in kwargs.keys()):
        return 200
    return 404


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

    @patch('config.config', side_effect=mocked_config_requests)
    def test_config_response(self, mock_get):
        """
        Test that incorrect endpoint returns an error
        """
        mock_get.return_value = 200
        self.assertEqual(mocked_config_requests(command='agencyList'), mock_get.return_value)
        self.assertEqual(mocked_config_requests(command='routeList', a='sf-muni'), mock_get.return_value)
        self.assertEqual(mocked_config_requests(command='routeConfig', a='sf-muni'), mock_get.return_value)
        self.assertEqual(mocked_config_requests(command='routeConfig', a='sf-muni', r='N'), mock_get.return_value)
        mock_get.return_value = 404
        self.assertEqual(mocked_config_requests(command='routeList'), mock_get.return_value)
        self.assertEqual(mocked_config_requests(command='routeConfig', r='N'), mock_get.return_value)

    @patch('message.message', side_effect=mocked_message_requests)
    def test_message_response(self, mock_get):
        """
        Test that incorrect endpoint returns an error
        """
        mock_get.return_value = 200
        self.assertEqual(mocked_message_requests(command='messages', a='sf-muni'), mock_get.return_value)
        self.assertEqual(mocked_message_requests(command='messages', a='sf-muni', r='N'), mock_get.return_value)
        mock_get.return_value = 404
        self.assertEqual(mocked_message_requests(command='messages', r='N'), mock_get.return_value)


if __name__ == '__main__':
    unittest.main()
