import unittest
from unittest import mock
from unittest.mock import patch

from pyqube.rest.clients import RestClient
from pyqube.rest.exceptions import (
    AlreadyAnsweringException,
    BadRequest,
    Forbidden,
    InactiveCounterException,
    InactiveQueueException,
    NoCurrentCounterException,
    NotAuthorized,
    NotFound,
)
from pyqube.types import Answering


@patch.object(RestClient, "post_request")
class TestCallNextTicketEndingCurrent(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        self.answering_data = {
            'id': 1,
            'ticket': {
                'id': 1,
                'signature': '1',
                'updated_at': '2024-01-01T00:00:00.000000Z',
                'number': 1,
                'printed_tag': 'A',
                'printed_number': '001',
                'note': None,
                'priority': False,
                'priority_level': 3,
                'created_at': '2024-01-01T00:00:00.000000Z',
                'state': 2,
                'is_generated_by_api_key': True,
                'invalidated_by_system': None,
                'ticket_local_runner': None,
                'tags': None,
                'queue': 1,
                'queue_dest': 1,
                'counter_dest': None,
                'profile_dest': None,
                'generated_by_ticket_kiosk': None,
                'generated_by_profile': None,
                'generated_by_api_key': 1,
                'local_runner': None
            },
            'transferred_from_answering': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'finish_reason': None,
            'started_at': '2024-01-01T00:00:00.000000Z',
            'finished_at': None,
            'invalidated_by_system': None,
            'waiting_time': 1,
            'service_time': None,
            'answering_local_runner': None,
            'profile': 1,
            'counter': 1,
            'queue': 1,
            'local_runner': None
        }

    def test_call_next_ticket_ending_current_with_success(self, mock_post_request):
        """Test call next ticket and checks if Answering object is returned"""
        profile_id = 1
        ticket_call_next_path = f"/locations/{self.location_id}/queue-management/profiles/{profile_id}/tickets/call-next/"

        mock_post_request.return_value.json.return_value = self.answering_data

        answering_created = self.qube_rest_client.get_queue_management_manager(
        ).call_next_ticket_ending_current(profile_id)
        mock_post_request.assert_called_once_with(ticket_call_next_path, params={
            'end_current': True
        })

        self.assertEqual(answering_created, Answering(**self.answering_data))

    def test_call_next_ticket_ending_current_for_bad_request(self, mock_post_request):
        """Test call next ticket to raises an Exception (BadRequest)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        mock_post_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_not_authorized(self, mock_post_request):
        """Test call next ticket to raises an Exception (NotAuthorized)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 401
        mock_post_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_forbidden(self, mock_post_request):
        """Test call next ticket to raises an Exception (Forbidden)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 403
        mock_post_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_not_found(self, mock_post_request):
        """Test call next ticket to raises an Exception (NotFound)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 404
        mock_post_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_already_answering_exception(self, mock_post_request):
        """Test call next ticket to raises an Exception (AlreadyAnsweringException)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "already_answering",
            "title": "Already answering a Ticket.",
            "detail": "Already answering a Ticket."
        }
        mock_post_request.return_value = response

        with self.assertRaises(AlreadyAnsweringException):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_not_current_counter_exception(self, mock_post_request):
        """Test call next ticket to raises an Exception (NoCurrentCounterException)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "no_associated_counter",
            "title": "This Profile does not have a current_counter in this Location.",
            "detail": "This Profile does not have a current_counter in this Location."
        }
        mock_post_request.return_value = response

        with self.assertRaises(NoCurrentCounterException):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_inactive_counter_exception(self, mock_post_request):
        """Test call next ticket to raises an Exception (InactiveCounterException)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "inactive_counter",
            "title": "The Counter that you are in is inactive.",
            "detail": "The Counter that you are in is inactive."
        }
        mock_post_request.return_value = response

        with self.assertRaises(InactiveCounterException):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)

    def test_call_next_ticket_ending_current_for_inactive_queue_exception(self, mock_post_request):
        """Test call next ticket to raises an Exception (InactiveQueueException)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "inactive_queue",
            "title": "Queue is inactive.",
            "detail": "Queue is inactive."
        }
        mock_post_request.return_value = response

        with self.assertRaises(InactiveQueueException):
            self.qube_rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)
