import requests

from qube.rest.queue_management import QueueManagementManager


class RestClient:
    """
    Client class to store some attributes needed to make requests to Qube
    """

    API_BASE_URL = "api.qube.q-better.com"

    def __init__(self, api_key: str, location_id: int, queue_management_manager: object = None, base_url: str = None):
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

    def get_request(self, path: str) -> object:
        """
        Makes a GET request to api. This method can be useful for Managers.
        """
        response = requests.get(self.base_url + path, headers=self.headers, timeout=10)
        return response

    def post_request(self, path: str, data: dict) -> object:
        """
        Makes a POST request to api. This method can be useful for Managers.
        """
        response = requests.post(self.base_url + path, headers=self.headers, data=data, timeout=10)
        return response

    def put_request(self, path: str, data: dict) -> object:
        """
        Makes a PUT request to api. This method can be useful for Managers.
        """
        response = requests.put(self.base_url + path, headers=self.headers, data=data, timeout=10)
        return response
