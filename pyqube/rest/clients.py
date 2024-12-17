import requests
from requests import Response

from typing import Union

from pyqube.rest.queue_management_manager import QueueManagementManager


class RestClient:
    """
    Client class for storing some attributes needed to make requests to Qube, getting queue management manager
    (default or not) and making some requests to API Server.
    """

    API_BASE_URL = "https://api.qube.q-better.com/en/api/v1"

    def __init__(self, api_key: str, location_id: int, queue_management_manager: object = None, base_url: str = None):
        """
        Initializes the Rest Client.
        Args:
            api_key (str): API key for client authentication.
            location_id (int): Location's id that will be used in requests.
            queue_management_manager (object, optional): Manager used on API Server interactions. Defaults to None.
            base_url (str, optional): Base url used on API interactions . Defaults to API_BASE_URL.
        """
        self.base_url = base_url or self.API_BASE_URL
        self.api_key = api_key
        self.headers = {
            "AUTHORIZATION": "Api-Key " + api_key,
        }
        self.location_id = location_id
        self.queue_management_manager = queue_management_manager

    def get_queue_management_manager(self) -> Union[QueueManagementManager, object]:
        """
        Returns Manager object. If client's queue management manager attribute is None, it returns default object of
        Queue Management Manager.
        Returns:
            object: Queue Management Manager object that will be able to make requests to API Server.
        """
        if self.queue_management_manager is None:
            self.queue_management_manager = QueueManagementManager(self)

        return self.queue_management_manager

    def get_request(self, path: str, params: dict = None) -> Response:
        """
        Makes a GET request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
        Returns:
            Response: Response returned from request.
        """
        response = requests.get(self.base_url + path, headers=self.headers, params=params, timeout=10)
        return response

    def post_request(self, path: str, params: dict = None, data: dict = None) -> Response:
        """
        Makes a POST request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
            data (dict): Data that will be sent in the body of the request.
        Returns:
            Response: Response returned from request.
        """
        response = requests.post(self.base_url + path, headers=self.headers, params=params, data=data, timeout=10)
        return response

    def put_request(self, path: str, params: dict = None, data: dict = None) -> Response:
        """
        Makes a PUT request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
            data (dict): Data that will be sent in the body of the request.
        Returns:
            Response: Response returned from request.
        """
        response = requests.put(self.base_url + path, headers=self.headers, params=params, data=data, timeout=10)
        return response

    def make_graphql_request(self, data: str = None) -> Response:
        """
        Mas a POST request to GraphQL endpoint. This method can be useful for Managers.
        Args:
            data (dict): Data that will be sent in the body of the request that defines the Response returned from
            GraphQL endpoint.
        Returns:
            Response: Response returned from request.
        """
        path = f"/graphql/"
        response = requests.post(self.base_url + path, headers=self.headers, json={
            "query": data
        }, timeout=10)
        return response
