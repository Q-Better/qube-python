import requests

from qube.rest.queue_management_manager import QueueManagementManager


class RestClient:
    """
    Client class for storing some attributes needed to make requests to Qube, getting queue management manager
    (default or not) and making some requests to API Server.
    """

    API_BASE_URL = "api.qube.q-better.com"

    def __init__(self, api_key: str, location_id: int, queue_management_manager: object = None, base_url: str = None):
        """
        Initializes and connects the Rest client.
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

    def get_queue_management_manager(self) -> object:
        """
        Returns Manager object. If client's queue management manager attribute is None, it returns default object of
        Queue Management Manager.
        """
        if self.queue_management_manager is None:
            self.queue_management_manager = QueueManagementManager(self)

        return self.queue_management_manager

    def get_request(self, path: str, params: dict = None) -> object:
        """
        Makes a GET request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
        """
        response = requests.get(self.base_url + path, headers=self.headers, params=params, timeout=10)
        return response

    def post_request(self, path: str, params: dict = None, data: dict = None) -> object:
        """
        Makes a POST request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
            data (dict): Data that will be sent in the body of the request.
        """
        response = requests.post(self.base_url + path, headers=self.headers, params=params, data=data, timeout=10)
        return response

    def put_request(self, path: str, params: dict = None, data: dict = None) -> object:
        """
        Makes a PUT request to API Server. This method can be useful for Managers.
        Args:
            path (str): Path of URL to be added to base url to make the request.
            params (dict): Query parameters that will be included in the URL.
            data (dict): Data that will be sent in the body of the request.
        """
        response = requests.put(self.base_url + path, headers=self.headers, params=params, data=data, timeout=10)
        return response
