import unittest
from unittest import mock
from unittest.mock import call, patch

from pyqube.rest.clients import RestClient
from pyqube.rest.exceptions import (
    BadRequest,
    Forbidden,
    NotAuthorized,
    NotFound,
)
from pyqube.types import Queue


@patch.object(RestClient, "get_request")
class TestListQueues(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        base_queue_fields = {
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
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

        self.list_of_queues_page_1 = [{
            'id': 1,
            'tag': 'A',
            'name': 'Queue A',
            **base_queue_fields
        }, {
            'id': 2,
            'tag': 'B',
            'name': 'Queue B',
            **base_queue_fields
        }, {
            'id': 3,
            'tag': 'C',
            'name': 'Queue C',
            **base_queue_fields
        }]

        self.list_of_queues_page_2 = [{
            'id': 4,
            'tag': 'D',
            'name': 'Queue D',
            **base_queue_fields
        }, {
            'id': 5,
            'tag': 'E',
            'name': 'Queue E',
            **base_queue_fields
        }, {
            'id': 6,
            'tag': 'F',
            'name': 'Queue F',
            **base_queue_fields
        }]

        self.queues_by_pages = [self.list_of_queues_page_1, self.list_of_queues_page_2]

        self.page_1_list_of_queues_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": self.list_of_queues_page_1
        }

        self.page_2_list_of_queues_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": self.list_of_queues_page_2
        }

    def test_list_queues_with_one_page_with_success(self, mock_get_request):
        # def test_list_queues_with_success(self):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        mock_get_request.return_value.json.return_value = self.page_1_list_of_queues_response

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()

        list_of_queues_generator = list(list_of_queues_generator)
        for page_with_queues in list_of_queues_generator:
            expected_queues_list = [Queue(**item) for item in self.queues_by_pages[0]]
            self.assertEqual(page_with_queues, expected_queues_list)

        mock_get_request.assert_called_once_with(list_queues_path, params={
            'page': 1,
            'page_size': 10
        })

    def test_list_queues_with_multiple_pages_with_success(self, mock_get_request):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        self.page_1_list_of_queues_response["next"] = f"https://api-url-qube.com{list_queues_path}?page=2"
        mock_get_request.return_value.json.side_effect = [
            self.page_1_list_of_queues_response, self.page_2_list_of_queues_response
        ]

        page_size = 3
        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues(page_size)
        page = 1

        for page_with_queues in list_of_queues_generator:
            expected_queues_list = [Queue(**item) for item in self.queues_by_pages[page - 1]]
            self.assertEqual(page_with_queues, expected_queues_list)
            page += 1

        mock_get_request.assert_has_calls([
            call(list_queues_path, params={
                'page': 1,
                'page_size': page_size
            }),
            call(list_queues_path, params={
                'page': 2,
                'page_size': page_size
            }),
        ],
                                          any_order=True)

    def test_list_queues_without_queues_with_success(self, mock_get_request):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        self.page_1_list_of_queues_response["results"] = []
        mock_get_request.return_value.json.return_value = self.page_1_list_of_queues_response

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()

        for page_with_queues in list_of_queues_generator:
            self.assertEqual(page_with_queues, [])

        mock_get_request.assert_called_once_with(list_queues_path, params={
            'page': 1,
            'page_size': 10
        })

    def test_list_queues_for_bad_request(self, mock_get_request):
        """Test list queues paginated to raises an Exception (BadRequest)"""
        response = mock.Mock()
        response.status_code = 400
        mock_get_request.return_value = response

        with self.assertRaises(BadRequest):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_for_not_authorized(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotAuthorized)"""
        response = mock.Mock()
        response.status_code = 401
        mock_get_request.return_value = response

        with self.assertRaises(NotAuthorized):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_for_forbidden(self, mock_get_request):
        """Test list queues paginated to raises an Exception (Forbidden)"""
        response = mock.Mock()
        response.status_code = 403
        mock_get_request.return_value = response

        with self.assertRaises(Forbidden):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_for_not_found(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotFound)"""
        response = mock.Mock()
        response.status_code = 404
        mock_get_request.return_value = response

        with self.assertRaises(NotFound):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass
