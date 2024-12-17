import json
import pytest
from unittest.mock import Mock

from pyqube.types import QueuingSystemReset


class TestQueuingSystemResetDecorator:
    """
    Test suite for the QueuingSystemResetHandler decorators.
    """

    @pytest.fixture
    def mqtt_client(self):
        """
        Fixture to create an instance of MQTTClient.
        """
        from pyqube.events.clients import MQTTClient
        return MQTTClient(api_key="dummy_api_key", location_id=1)

    def simulate_mqtt_message(self, mqtt_client, topic, payload):
        """
        Helper method to simulate an MQTT message.

        Args:
            mqtt_client (MQTTClient): The MQTT client instance.
            topic (str): The MQTT topic.
            payload (dict): The payload for the MQTT message.
        """
        mqtt_client._on_message(
            mqtt_client.client, None, Mock(topic=topic, payload=json.dumps(payload).encode('utf-8'))
        )

    def test_on_queuing_system_resets_created(self, mqtt_client):
        """
        Test the on_queuing_system_resets_created decorator.
        """
        handler_mock = Mock()
        payload = {
            "id": 123,
            "created_at": "2024-11-25T12:00:00Z",
            "location": 1
        }

        @mqtt_client.on_queuing_system_resets_created()
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queuing-system-resets/created"
        self.simulate_mqtt_message(mqtt_client, topic, payload)

        handler_mock.assert_called_once_with(QueuingSystemReset(**payload))
