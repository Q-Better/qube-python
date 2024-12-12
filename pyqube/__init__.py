from pyqube.events.clients import MQTTClient
from pyqube.rest.clients import RestClient


class QubeClient(MQTTClient, RestClient):
    """
    A unified client that combines both MQTT and REST capabilities.
    It supports interacting with MQTT brokers for real-time messaging and with a REST API for general requests.
    """

    def __init__(
        self,
        api_key: str,
        location_id: int,
        broker_url: str = None,
        broker_port: int = None,
        base_url: str = None,
        queue_management_manager: object = None
    ):
        """
        Initializes the QubeClient by setting up both MQTT and REST components.

        Args:
            api_key (str): API key for client authentication.
            location_id (int): Location ID to use in requests.
            broker_url (str, optional): URL of the MQTT broker. Defaults to MQTTClient.DEFAULT_BROKER_URL.
            broker_port (int, optional): Port of the MQTT broker. Defaults to MQTTClient.DEFAULT_BROKER_PORT.
            base_url (str, optional): Base URL for REST API requests. Defaults to RestClient.API_BASE_URL.
            queue_management_manager (object, optional): Manager used for queue management via REST API.
        """
        MQTTClient.__init__(self, api_key, location_id, broker_url, broker_port)
        RestClient.__init__(self, api_key, location_id, queue_management_manager, base_url)
