import unittest
from unittest import mock
from unittest.mock import patch

from pyqube.rest.clients import RestClient
from pyqube.rest.exceptions import (
    BadRequest,
    Forbidden,
    NotAuthorized,
    NotFound,
)
from pyqube.types import Answering


@patch.object(RestClient, "get_request")
class TestGetCurrentAnswering(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
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

    def test_get_current_answering_with_success(self, mock_get_request):
        """Test get current answering and checks if Answering object is returned"""
        profile_id = 1
        end_answering_path = f"/locations/{self.location_id}/queue-management/profiles/{profile_id}/answerings/current/"

        mock_get_request.return_value.json.return_value = self.answering_data

        answering_ended = self.qube_rest_client.get_queue_management_manager().get_current_answering(profile_id)
        mock_get_request.assert_called_once_with(end_answering_path)

        self.assertEqual(answering_ended, Answering(**self.answering_data))

    def test_get_current_answering_for_bad_request(self, mock_get_request):
        """Test get current answering to raises an Exception (BadRequest)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 400
        mock_get_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().get_current_answering(profile_id)

    def test_get_current_answering_for_not_authorized(self, mock_get_request):
        """Test get current answering to raises an Exception (NotAuthorized)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 401
        mock_get_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().get_current_answering(profile_id)

    def test_get_current_answering_for_forbidden(self, mock_get_request):
        """Test get current answering to raises an Exception (Forbidden)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 403
        mock_get_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().get_current_answering(profile_id)

    def test_get_current_answering_for_not_found(self, mock_get_request):
        """Test get current answering to raises an Exception (NotFound)"""
        profile_id = 1

        response = mock.Mock()
        response.status_code = 404
        mock_get_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().get_current_answering(profile_id)
