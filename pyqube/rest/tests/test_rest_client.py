import requests

import unittest
from unittest.mock import Mock, patch

from pyqube.rest.clients import RestClient
from pyqube.rest.queue_management_manager import QueueManagementManager


class TestRestClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

    def test_initialization_with_correct_credentials(self):
        """Test that the client initializes with correct credentials"""
        self.assertEqual(self.qube_rest_client.base_url, self.base_url)
        self.assertEqual(self.qube_rest_client.api_key, self.api_key)
        self.assertEqual(self.qube_rest_client.location_id, self.location_id)

    def test_initialization_with_default_base_url(self):
        """Test that the client initializes with base url without this argument"""
        qube_rest_client = RestClient(self.api_key, self.location_id)
        self.assertEqual(qube_rest_client.base_url, "https://api.qube.q-better.com/en/api/v1")

    def test_get_queue_management_manager_with_default_manager(self):
        """Test that the client gets the default queue management manager"""
        queue_management_manager = self.qube_rest_client.get_queue_management_manager()

        self.assertIsInstance(queue_management_manager, QueueManagementManager)

    def test_get_queue_management_manager_with_custom_manager(self):
        """Test that the client gets the custom queue management manager"""
        custom_queue_management_manager = Mock()
        qube_rest_client = RestClient(
            self.api_key,
            self.location_id,
            queue_management_manager=custom_queue_management_manager,
            base_url=self.base_url
        )
        queue_management_manager_returned = qube_rest_client.get_queue_management_manager()

        self.assertEqual(custom_queue_management_manager, queue_management_manager_returned)

    @patch.object(requests, "get")
    def test_get_request(self, mock_requests_get):
        """Test the get request method"""
        path = "/path/to/request"
        params = {
            "some_param": "some_value"
        }
        self.qube_rest_client.get_request(path, params)
        mock_requests_get.assert_called_once_with(
            self.base_url + path, headers=self.qube_rest_client.headers, params=params, timeout=10
        )

    @patch.object(requests, "post")
    def test_post_request(self, mock_requests_get):
        """Test the post request method"""
        path = "/path/to/request"
        params = {
            "some_param": "some_value"
        }
        data = {
            "some_key": "some_value"
        }
        self.qube_rest_client.post_request(path, params, data)
        mock_requests_get.assert_called_once_with(
            self.base_url + path, headers=self.qube_rest_client.headers, params=params, data=data, timeout=10
        )

    @patch.object(requests, "put")
    def test_put_request(self, mock_requests_get):
        """Test the post request method"""
        path = "/path/to/request"
        params = {
            "some_param": "some_value"
        }
        data = {
            "some_key": "some_value"
        }
        self.qube_rest_client.put_request(path, params, data)
        mock_requests_get.assert_called_once_with(
            self.base_url + path, headers=self.qube_rest_client.headers, params=params, data=data, timeout=10
        )
