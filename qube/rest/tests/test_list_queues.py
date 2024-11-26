import unittest
from unittest import mock
from unittest.mock import call, patch

from qube.rest.clients import RestClient
from qube.rest.exceptions import BadRequest, Forbidden, NotAuthorized, NotFound


class TestListQueues(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1

        self.qube_rest_client = RestClient(self.api_key, self.location_id, base_url=self.base_url)

        self.list_of_queues_page_1 = [{
            'id': 1,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
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
        }, {
            'id': 2,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'tag': 'B',
            'name': 'Queue B',
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
        }, {
            'id': 3,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'tag': 'C',
            'name': 'Queue C',
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
        }]

        self.list_of_queues_page_2 = [{
            'id': 4,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'tag': 'D',
            'name': 'Queue D',
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
        }, {
            'id': 5,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'tag': 'E',
            'name': 'Queue E',
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
        }, {
            'id': 6,
            'is_active': True,
            'deleted_at': None,
            'created_at': '2024-01-01T00:00:00.000000Z',
            'updated_at': '2024-01-01T00:00:00.000000Z',
            'tag': 'F',
            'name': 'Queue F',
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
        }]

        self.queues_by_pages = [self.list_of_queues_page_1, self.list_of_queues_page_2]

        self.page_1_list_queues_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": self.list_of_queues_page_1
        }

        self.page_2_list_queues_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": self.list_of_queues_page_2
        }

    @patch.object(RestClient, "get_request")
    def test_list_queues_with_one_page_with_success(self, mock_get_request):
        # def test_list_queues_with_success(self):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        mock_get_request.return_value.json.return_value = self.page_1_list_queues_response

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()

        list_of_queues_generator = list(list_of_queues_generator)
        for page_with_queues in list_of_queues_generator:
            self.assertEqual(page_with_queues, self.queues_by_pages[0])

        mock_get_request.assert_called_once_with(list_queues_path, params={
            'page': 1
        })

    @patch.object(RestClient, "get_request")
    def test_list_queues_with_multiple_pages_with_success(self, mock_get_request):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        self.page_1_list_queues_response["next"] = f"https://api-url-qube.com{list_queues_path}?page=2"
        mock_get_request.return_value.json.side_effect = [
            self.page_1_list_queues_response, self.page_2_list_queues_response
        ]

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
        page = 1

        for page_with_queues in list_of_queues_generator:
            self.assertEqual(page_with_queues, self.queues_by_pages[page - 1])
            page += 1

        mock_get_request.assert_has_calls([
            call(list_queues_path, params={
                'page': 1
            }),
            call(list_queues_path, params={
                'page': 2
            }),
        ],
                                          any_order=True)

    @patch.object(RestClient, "get_request")
    def test_list_queues_without_queues_with_success(self, mock_get_request):
        """Test list queues paginated and checks if a list of Queues is returned"""
        list_queues_path = f"/locations/{self.location_id}/queues/"

        self.page_1_list_queues_response["results"] = []
        mock_get_request.return_value.json.return_value = self.page_1_list_queues_response

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()

        for page_with_queues in list_of_queues_generator:
            self.assertEqual(page_with_queues, [])

        mock_get_request.assert_called_once_with(list_queues_path, params={
            'page': 1
        })

    @patch.object(RestClient, "get_request")
    def test_list_queues_for_bad_request(self, mock_get_request):
        """Test list queues paginated to raises an Exception (BadRequest)"""
        response = mock.Mock()
        response.status_code = 400
        mock_get_request.return_value = response

        with self.assertRaises(BadRequest):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    @patch.object(RestClient, "get_request")
    def test_list_queues_for_not_authorized(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotAuthorized)"""
        response = mock.Mock()
        response.status_code = 401
        mock_get_request.return_value = response

        with self.assertRaises(NotAuthorized):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    @patch.object(RestClient, "get_request")
    def test_list_queues_for_forbidden(self, mock_get_request):
        """Test list queues paginated to raises an Exception (Forbidden)"""
        response = mock.Mock()
        response.status_code = 403
        mock_get_request.return_value = response

        with self.assertRaises(Forbidden):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass

    @patch.object(RestClient, "get_request")
    def test_list_queues_for_not_found(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotFound)"""
        response = mock.Mock()
        response.status_code = 404
        mock_get_request.return_value = response

        with self.assertRaises(NotFound):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues()
            for _ in list_of_queues_generator:
                pass
