import base64
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
from pyqube.rest.graphql_generators import QueuesListGraphQLGenerator
from pyqube.types import Queue


@patch.object(RestClient, "make_graphql_request")
class TestListQueuesOfQueuesList(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api-url-qube.com"
        self.api_key = 'api_key'
        self.location_id = 1
        self.location_id_encoded = base64.b64encode(f"LocationNode:{self.location_id}".encode('utf-8')).decode('utf-8')
        self.queues_list_id = 1

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
            'schedule': None
        }

        ids_encoded_list = [
            base64.b64encode(f'QueueNode:{queue_id}'.encode('utf-8')).decode('utf-8') for queue_id in range(1, 7)
        ]
        tags_list = ['A', 'B', 'C', 'D', 'E', 'F']
        names_list = ['Queue A', 'Queue B', 'Queue C', 'Queue D', 'Queue E', 'Queue F']

        self.list_of_queues_page_1 = [{
            'id': ids_encoded_list[index],
            'tag': tags_list[index],
            'name': names_list[index],
            'location': {
                'id': self.location_id_encoded
            },
            **base_queue_fields
        } for index in range(0, 3)]

        self.list_of_queues_page_2 = [{
            'id': ids_encoded_list[index],
            'tag': tags_list[index],
            'name': names_list[index],
            'location': {
                'id': self.location_id_encoded
            },
            **base_queue_fields
        } for index in range(3, 6)]

        self.queues_by_pages = [self.list_of_queues_page_1, self.list_of_queues_page_2]

        self.page_1_list_of_queues_of_queues_list_response = {
            'data': {
                'queues_lists_queues': {
                    'edges': [{
                        'cursor': 'random_graphql_cursor_1',
                        'node': {
                            'id': 'random_graphql_node_1',
                            'queue': self.list_of_queues_page_1[0]
                        }
                    }, {
                        'cursor': 'random_graphql_cursor_2',
                        'node': {
                            'id': 'random_graphql_node_2',
                            'queue': self.list_of_queues_page_1[1]
                        }
                    }, {
                        'cursor': 'random_graphql_cursor_3',
                        'node': {
                            'id': 'random_graphql_node_3',
                            'queue': self.list_of_queues_page_1[2]
                        }
                    }],
                    'pageInfo': {
                        'endCursor': 'end_cursor_1',
                        'hasNextPage': False,
                        'hasPreviousPage': False,
                        'startCursor': 'start_cursor_1'
                    }
                }
            }
        }

        self.page_2_list_of_queues_of_queues_list_response = {
            'data': {
                'queues_lists_queues': {
                    'edges': [{
                        'cursor': 'random_graphql_cursor_4',
                        'node': {
                            'id': 'random_graphql_node_4',
                            'queue': self.list_of_queues_page_2[0]
                        }
                    }, {
                        'cursor': 'random_graphql_cursor_5',
                        'node': {
                            'id': 'random_graphql_node_5',
                            'queue': self.list_of_queues_page_2[1]
                        }
                    }, {
                        'cursor': 'random_graphql_cursor_6',
                        'node': {
                            'id': 'random_graphql_node_6',
                            'queue': self.list_of_queues_page_2[2]
                        }
                    }],
                    'pageInfo': {
                        'endCursor': 'end_cursor_2',
                        'hasNextPage': False,
                        'hasPreviousPage': False,
                        'startCursor': 'start_cursor_2'
                    }
                }
            }
        }

    @classmethod
    def _convert_encoded_json_to_queue(cls, item):
        item["id"] = int(base64.b64decode(item["id"]).decode('utf-8').split(":")[1])
        item["location"] = int(base64.b64decode(item["location"]["id"]).decode('utf-8').split(":")[1])
        if item.get("schedule"):
            item["schedule"] = int(base64.b64decode(item["schedule"]["id"]).decode('utf-8').split(":")[1])
        return Queue(**item)

    def test_list_queues_of_queues_list_with_one_page_with_success(self, mock_make_graphql_request):
        # def test_list_queues_of_queues_list_with_success(self):
        """Test list queues paginated and checks if a list of Queues is returned"""
        mock_make_graphql_request.return_value.json.return_value = self.page_1_list_of_queues_of_queues_list_response

        list_of_queues_of_queues_list_generator = self.qube_rest_client.get_queue_management_manager(
        ).list_queues_of_queues_list(self.queues_list_id)

        for page_with_queues in list_of_queues_of_queues_list_generator:
            expected_queues_list = [
                Queue(**item['node']['queue'])
                for item in self.page_1_list_of_queues_of_queues_list_response['data']['queues_lists_queues']['edges']
            ]
            self.assertEqual(page_with_queues, expected_queues_list)

        expected_query = QueuesListGraphQLGenerator.generate_query_body(
            queues_list=self.queues_list_id, first=10, after="\"\""
        )
        mock_make_graphql_request.assert_called_once_with(expected_query)

    def test_list_queues_of_queues_list_with_multiple_pages_with_success(self, mock_make_graphql_request):
        """Test list queues paginated and checks if a list of Queues is returned"""
        self.page_1_list_of_queues_of_queues_list_response["data"]["queues_lists_queues"]["pageInfo"]["hasNextPage"
                                                                                                      ] = True
        mock_make_graphql_request.return_value.json.side_effect = [
            self.page_1_list_of_queues_of_queues_list_response, self.page_2_list_of_queues_of_queues_list_response
        ]

        page_size = 3
        list_of_queues_of_queues_list_generator = self.qube_rest_client.get_queue_management_manager(
        ).list_queues_of_queues_list(self.queues_list_id, page_size)

        expected_queues_list_pages = [[
            self._convert_encoded_json_to_queue(item.copy()) for item in self.queues_by_pages[0]
        ], [self._convert_encoded_json_to_queue(item.copy()) for item in self.queues_by_pages[1]]]
        page = 1
        for page_with_queues in list_of_queues_of_queues_list_generator:
            self.assertEqual(page_with_queues, expected_queues_list_pages[page - 1])
            page += 1

        mock_make_graphql_request.assert_has_calls([
            call(
                QueuesListGraphQLGenerator.generate_query_body(
                    queues_list=self.queues_list_id, first=page_size, after="\"\""
                )
            ),
            call(
                QueuesListGraphQLGenerator.generate_query_body(
                    queues_list=self.queues_list_id, first=page_size, after="\"end_cursor_1\""
                )
            ),
        ],
                                                   any_order=True)

    def test_list_queues_of_queues_list_without_queues_with_success(self, mock_make_graphql_request):
        """Test list queues paginated and checks if a list of Queues is returned"""

        self.page_1_list_of_queues_of_queues_list_response["data"]["queues_lists_queues"]["edges"] = []
        mock_make_graphql_request.return_value.json.return_value = self.page_1_list_of_queues_of_queues_list_response

        list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues_of_queues_list(
            self.queues_list_id
        )

        for page_with_queues in list_of_queues_generator:
            self.assertEqual(page_with_queues, [])

        expected_query = QueuesListGraphQLGenerator.generate_query_body(
            queues_list=self.queues_list_id, first=10, after="\"\""
        )
        mock_make_graphql_request.assert_called_once_with(expected_query)

    def test_list_queues_of_queues_list_for_bad_request(self, mock_get_request):
        """Test list queues paginated to raises an Exception (BadRequest)"""
        response = mock.Mock()
        response.status_code = 400
        mock_get_request.return_value = response

        with self.assertRaises(BadRequest):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues_of_queues_list(
                self.queues_list_id
            )
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_of_queues_list_for_not_authorized(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotAuthorized)"""
        response = mock.Mock()
        response.status_code = 401
        mock_get_request.return_value = response

        with self.assertRaises(NotAuthorized):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues_of_queues_list(
                self.queues_list_id
            )
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_of_queues_list_for_forbidden(self, mock_get_request):
        """Test list queues paginated to raises an Exception (Forbidden)"""
        response = mock.Mock()
        response.status_code = 403
        mock_get_request.return_value = response

        with self.assertRaises(Forbidden):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues_of_queues_list(
                self.queues_list_id
            )
            for _ in list_of_queues_generator:
                pass

    def test_list_queues_of_queues_list_for_not_found(self, mock_get_request):
        """Test list queues paginated to raises an Exception (NotFound)"""
        response = mock.Mock()
        response.status_code = 404
        mock_get_request.return_value = response

        with self.assertRaises(NotFound):
            list_of_queues_generator = self.qube_rest_client.get_queue_management_manager().list_queues_of_queues_list(
                self.queues_list_id
            )
            for _ in list_of_queues_generator:
                pass
