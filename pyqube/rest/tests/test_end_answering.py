import unittest
from unittest import mock
from unittest.mock import patch

from pyqube.rest.clients import RestClient
from pyqube.rest.exceptions import (
    AnsweringAlreadyProcessedException,
    BadRequest,
    Forbidden,
    HasLocalRunnerException,
    InactiveCounterException,
    InactiveQueueException,
    MismatchingCountersException,
    NoCurrentCounterException,
    NotAuthorized,
    NotFound,
)
from pyqube.types import Answering


@patch.object(RestClient, "put_request")
class TestEndAnswering(unittest.TestCase):

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
            'finish_reason': 6,
            'started_at': '2024-01-01T00:00:00.000000Z',
            'finished_at': None,
            'invalidated_by_system': None,
            'waiting_time': 1,
            'service_time': 1,
            'answering_local_runner': None,
            'profile': 1,
            'counter': 1,
            'queue': 1,
            'local_runner': None
        }

    def test_end_answering_with_success(self, mock_put_request):
        """Test end answering and checks if Answering object is returned"""
        profile_id = 1
        answering_id = 1
        end_answering_path = f"/locations/{self.location_id}/queue-management/profiles/{profile_id}/answerings/{answering_id}/end/"

        mock_put_request.return_value.json.return_value = self.answering_data

        answering_ended = self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)
        mock_put_request.assert_called_once_with(end_answering_path)

        self.assertEqual(answering_ended, Answering(**self.answering_data))

    def test_end_answering_for_bad_request(self, mock_put_request):
        """Test end answering to raises an Exception (BadRequest)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        mock_put_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_not_authorized(self, mock_put_request):
        """Test end answering to raises an Exception (NotAuthorized)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 401
        mock_put_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_forbidden(self, mock_put_request):
        """Test end answering to raises an Exception (Forbidden)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 403
        mock_put_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_not_found(self, mock_put_request):
        """Test end answering to raises an Exception (NotFound)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 404
        mock_put_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_already_processed_exception(self, mock_put_request):
        """Test end answering to raises an Exception (AnsweringAlreadyProcessedException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "already_processed",
            "title": "Answering is already processed and finished.",
            "detail": "Answering is already processed and finished."
        }
        mock_put_request.return_value = response

        with self.assertRaises(AnsweringAlreadyProcessedException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_no_current_counter_exception(self, mock_put_request):
        """Test end answering to raises an Exception (AnsweringAlreadyProcessedException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "no_associated_counter",
            "title": "This Profile does not have a current_counter in this Location.",
            "detail": "This Profile does not have a current_counter in this Location."
        }
        mock_put_request.return_value = response

        with self.assertRaises(NoCurrentCounterException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_inactive_counter_exception(self, mock_put_request):
        """Test end answering to raises an Exception (AnsweringAlreadyProcessedException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "inactive_counter",
            "title": "The Counter that you are in is inactive.",
            "detail": "The Counter that you are in is inactive."
        }
        mock_put_request.return_value = response

        with self.assertRaises(InactiveCounterException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_mismatching_counters_exception(self, mock_put_request):
        """Test end answering to raises an Exception (MismatchingCountersException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "mismatching_counters",
            "title": "The Counter of Answering is not the current_counter of Profile.",
            "detail": "The Counter of Answering is not the current_counter of Profile."
        }
        mock_put_request.return_value = response

        with self.assertRaises(MismatchingCountersException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_mismatching_counters_exception(self, mock_put_request):
        """Test end answering to raises an Exception (InactiveQueueException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "inactive_queue",
            "title": "Queue is inactive.",
            "detail": "Queue is inactive."
        }
        mock_put_request.return_value = response

        with self.assertRaises(InactiveQueueException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)

    def test_end_answering_for_has_local_runner_exception(self, mock_put_request):
        """Test end answering to raises an Exception (MismatchingCountersException)"""
        profile_id = 1
        answering_id = 1

        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "local_runner_error",
            "sub_type": "has_local_runner",
            "title": "This Location has Local Runner set: Queue Management action should be done through it.",
            "detail": "This Location has Local Runner set: Queue Management action should be done through it."
        }
        mock_put_request.return_value = response

        with self.assertRaises(HasLocalRunnerException):
            self.qube_rest_client.get_queue_management_manager().end_answering(profile_id, answering_id)
