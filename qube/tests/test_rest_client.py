import unittest
from unittest.mock import Mock

from qube.rest.clients import RestClient
from qube.rest.queue_management import QueueManagementManager


class TestRestClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.base_url, self.api_key, self.location_id)

    def test_initialization_with_correct_credentials(self):
        """Test that the client initializes with correct credentials"""
        self.assertEqual(self.qube_rest_client.base_url, self.base_url)
        self.assertEqual(self.qube_rest_client.api_key, self.api_key)
        self.assertEqual(self.qube_rest_client.location_id, self.location_id)

    def test_get_queue_management_manager_with_default_manager(self):
        """Test that the client gets the default queue management manager"""
        queue_management_manager = self.qube_rest_client.get_queue_management_manager()

        self.assertIsInstance(queue_management_manager, QueueManagementManager)

    def test_get_queue_management_manager_with_custom_manager(self):
        """Test that the client gets the custom queue management manager"""
        custom_queue_management_manager = Mock()
        qube_rest_client = RestClient(
            self.base_url, self.api_key, self.location_id, queue_management_manager=custom_queue_management_manager
        )
        queue_management_manager_returned = qube_rest_client.get_queue_management_manager()

        self.assertEqual(custom_queue_management_manager, queue_management_manager_returned)
