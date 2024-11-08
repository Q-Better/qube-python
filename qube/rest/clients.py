from qube.rest.queue_management import QueueManagementManager


class RestClient:
    """
    Client class to store some attributes needed to make requests to Qube
    """

    def __init__(self, base_url: str, api_key: str, location_id: int, queue_management_manager: object = None):
        self.base_url = base_url
        self.api_key = api_key
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
