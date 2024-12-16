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
from pyqube.types import LocationAccessWithCurrentCounter


@patch.object(RestClient, "put_request")
class TestSetCurrentCounter(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1
        self.location_access_id = 1
        self.counter_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        self.location_access_with_counter_data = {
            'id': self.location_access_id,
            'location': self.location_id,
            'profile': 1,
            'current_counter': {
                'id': self.counter_id,
                'is_active': True,
                'deleted_at': None,
                'created_at': '2024-01-01T00:00:00.000000Z',
                'updated_at': '2024-01-01T00:00:00.000000Z',
                'tag': 'A',
                'name': 'Counter 1',
                'location': self.location_id
            },
            'groups': [1],
            'invitation_email': 'email@example.com',
            'status': 2,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'deleted_at': None,
        }

    def test_set_current_counter_with_success(self, mock_put_request):
        """Test set current counter and checks if LocationAccess with current Counter object is returned"""
        set_current_counter_path = f"/locations/{self.location_id}/location-accesses/{self.location_access_id}/associate-counter/"

        mock_put_request.return_value.json.return_value = self.location_access_with_counter_data

        location_access_updated = self.qube_rest_client.get_queue_management_manager().set_current_counter(
            self.location_access_id, self.counter_id
        )
        mock_put_request.assert_called_once_with(set_current_counter_path, data={
            'counter': self.counter_id
        })

        self.assertEqual(
            location_access_updated, LocationAccessWithCurrentCounter(**self.location_access_with_counter_data)
        )

    def test_set_current_counter_for_bad_request(self, mock_put_request):
        """Test set current counter to raises an Exception (BadRequest)"""
        response = mock.Mock()
        response.status_code = 400
        mock_put_request.return_value = response

        with self.assertRaises(BadRequest):
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )

    def test_set_current_counter_for_not_authorized(self, mock_put_request):
        """Test set current counter to raises an Exception (NotAuthorized)"""
        response = mock.Mock()
        response.status_code = 401
        mock_put_request.return_value = response

        with self.assertRaises(NotAuthorized):
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )

    def test_set_current_counter_for_forbidden(self, mock_put_request):
        """Test set current counter to raises an Exception (Forbidden)"""
        response = mock.Mock()
        response.status_code = 403
        mock_put_request.return_value = response

        with self.assertRaises(Forbidden):
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )

    def test_set_current_counter_for_not_found(self, mock_put_request):
        """Test set current counter to raises an Exception (NotFound)"""
        response = mock.Mock()
        response.status_code = 404
        mock_put_request.return_value = response

        with self.assertRaises(NotFound):
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )

    def test_set_current_counter_for_no_access_to_counter_exception(self, mock_put_request):
        """Test set current counter to raises an Exception (NoAccessToCounterException)"""
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
            self.qube_rest_client.get_queue_management_manager().set_current_counter(
                self.location_access_id, self.counter_id
            )
