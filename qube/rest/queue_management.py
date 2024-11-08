import requests


class QueueManagementManager:
    """
    Manager class that offers some methods about Queue management.
    """

    def __init__(self, client: object):
        self.client = client
