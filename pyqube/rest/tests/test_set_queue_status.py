import unittest
from unittest import mock
from unittest.mock import patch

from pyqube.rest.clients import RestClient
from pyqube.rest.exceptions import (
    BadRequest,
    Forbidden,
    NoAccessToCounterException,
    NotAuthorized,
    NotFound,
)
from pyqube.types import Queue


@patch.object(RestClient, "put_request")
class TestSetQueueStatus(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1
        self.location_access_id = 1
        self.counter_id = 1
        self.queue_id = 1
        self.is_active = True

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        self.queue_data = {
            'id': self.queue_id,
            'is_active': True,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'deleted_at': None,
            'tag': 'A',
            'name': 'Queue A',
            'allow_priority': True,
            'ticket_range_enabled': False,
            'min_ticket_number': 1,
            'max_ticket_number': 99,
            'ticket_tolerance_enabled': False,
            'ticket_tolerance_number': 1,
            'kpi_wait_count': 1,
            'kpi_wait_time': 60,
            'kpi_service_time': 120,
            'location': self.location_id,
            'schedule': None
        }

    def test_set_queue_status_with_success(self, mock_put_request):
        """Test set queue status and checks if Queue object is returned"""
        queue_id = 1
        set_queue_status_path = f"/locations/{self.location_id}/queues/{queue_id}/status/"

        mock_put_request.return_value.json.return_value = self.queue_data

        location_access_updated = self.qube_rest_client.get_queue_management_manager().set_queue_status(
            self.queue_id, self.is_active
        )
        mock_put_request.assert_called_once_with(set_queue_status_path, data={
            'is_active': self.is_active
        })

        self.assertEqual(location_access_updated, Queue(**self.queue_data))

    def test_set_queue_status_for_bad_request(self, mock_put_request):
        """Test set queue status to raises an Exception (BadRequest)"""
        response = mock.Mock()
        response.status_code = 400
        mock_put_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().set_queue_status(self.queue_id, self.is_active)

    def test_set_queue_status_for_not_authorized(self, mock_put_request):
        """Test set queue status to raises an Exception (NotAuthorized)"""
        response = mock.Mock()
        response.status_code = 401
        mock_put_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().set_queue_status(self.queue_id, self.is_active)

    def test_set_queue_status_for_forbidden(self, mock_put_request):
        """Test set queue status to raises an Exception (Forbidden)"""
        response = mock.Mock()
        response.status_code = 403
        mock_put_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().set_queue_status(self.queue_id, self.is_active)

    def test_set_queue_status_for_not_found(self, mock_put_request):
        """Test set queue status to raises an Exception (NotFound)"""
        response = mock.Mock()
        response.status_code = 404
        mock_put_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )

    def test_set_queue_status_for_no_access_to_counter_exception(self, mock_put_request):
        """Test set queue status to raises an Exception (NoAccessToCounterException)"""
        response = mock.Mock()
        response.status_code = 400
        response.json.return_value = {
            "status": 400,
            "type": "queue_management_error",
            "sub_type": "counter_not_associated",
            "title": "This Profile is not associated to this Counter.",
            "detail": "This Profile is not associated to this Counter."
        }
        mock_put_request.return_value = response

        with self.assertRaises(NoAccessToCounterException):
            self.qube_rest_client.get_queue_management_manager().set_queue_status(self.queue_id, self.is_active)
