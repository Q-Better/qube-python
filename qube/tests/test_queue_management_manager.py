import unittest
from unittest import mock
from unittest.mock import patch

from qube.rest.clients import RestClient
from qube.rest.exceptions import BadRequest, Forbidden, NotAuthorized, NotFound
from qube.rest.types import Ticket


class TestQueueManagementManager(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        self.ticket_data = {
            "id": 13920,
            "signature": '88',
            "number": 18,
            "printed_number": '018',
            "printed_tag": 'AS',
            "queue": 1,
            "queue_dest": 1,
            "counter_dest": None,
            "profile_dest": None,
            "state": 1,
            "generated_by_ticket_kiosk": None,
            "generated_by_profile": None,
            "generated_by_api_key": 1,
            "priority": False,
            "priority_level": 3,
            "note": None,
            "updated_at": '2024-01-01T00:00:00.000000Z',
            "created_at": '2024-01-01T00:00:00.000000Z',
            "is_generated_by_api_key": True,
            "invalidated_by_system": None,
            "ticket_local_runner": None,
            "tags": None,
            "local_runner": None
        }

    @patch.object(RestClient, "post_request")
    def test_generate_ticket_with_success(self, mock_post_request):
        """Test generate ticket and checks if Ticket object is returned"""

        queue_id = 1
        priority = True
        ticket_generate_path = f"/locations/{self.location_id}/queue-management/tickets/generate/"
        generate_ticket_data = {
            "queue": queue_id,
            "priority": priority
        }

        mock_post_request.return_value.json.return_value = self.ticket_data

        ticket_generated = self.qube_rest_client.get_queue_management_manager().generate_ticket(queue_id, priority)
        mock_post_request.assert_called_once_with(ticket_generate_path, data=generate_ticket_data)

        self.assertEqual(ticket_generated, Ticket(**self.ticket_data))

    @patch.object(RestClient, "post_request")
    def test_generate_ticket_for_bad_request(self, mock_post_request):
        """Test generate ticket to raises an Exception (BadRequest)"""
        queue_id = 1
        priority = True

        response = mock.Mock()
        response.status_code = 400
        mock_post_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().generate_ticket(queue_id, priority)

    @patch.object(RestClient, "post_request")
    def test_generate_ticket_for_not_authorized(self, mock_post_request):
        """Test generate ticket to raises an Exception (NotAuthorized)"""
        queue_id = 1
        priority = True

        response = mock.Mock()
        response.status_code = 401
        mock_post_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().generate_ticket(queue_id, priority)

    @patch.object(RestClient, "post_request")
    def test_generate_ticket_for_forbidden(self, mock_post_request):
        """Test generate ticket to raises an Exception (Forbidden)"""
        queue_id = 1
        priority = True

        response = mock.Mock()
        response.status_code = 403
        mock_post_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().generate_ticket(queue_id, priority)

    @patch.object(RestClient, "post_request")
    def test_generate_ticket_for_not_found(self, mock_post_request):
        """Test generate ticket to raises an Exception (NotFound)"""
        queue_id = 1
        priority = True

        response = mock.Mock()
        response.status_code = 404
        mock_post_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().generate_ticket(queue_id, priority)
