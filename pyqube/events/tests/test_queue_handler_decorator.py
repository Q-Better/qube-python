import json
import pytest
from unittest.mock import Mock

from pyqube.types import (
    QueueGeneralDetails,
    QueueWithAverageWaitingTime,
    QueueWithWaitingTickets,
)


class TestQueueHandlerDecorators:
    """
    Test suite for the QueueHandler decorators using the mqtt_client fixture.
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

    def test_on_queues_changed_average_waiting_time_specific_queue(self, mqtt_client):
        """
        Test the on_queues_changed_average_waiting_time decorator for a specific queue ID.
        """
        handler_mock = Mock()

        payload = {
            "queue": {
                "id": 42,
                "tag": "A",
                "name": "Main Queue",
                "kpi_wait_count": 5,
                "kpi_wait_time": 10,
                "kpi_service_time": 15
            },
            "average_waiting_time": 5
        }

        @mqtt_client.on_queues_changed_average_waiting_time(queue_id=42)
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queues/changed-average-waiting-time"
        self.simulate_mqtt_message(mqtt_client, topic, [payload])

        handler_mock.assert_called_once_with(QueueWithAverageWaitingTime(**payload))

    def test_on_queues_changed_average_waiting_time_all_queues(self, mqtt_client):
        """
        Test the on_queues_changed_average_waiting_time decorator for all queues.
        """
        handler_mock = Mock()
        payload = {
            "queue": {
                "id": 42,
                "tag": "A",
                "name": "Main Queue",
                "kpi_wait_count": 5,
                "kpi_wait_time": 10,
                "kpi_service_time": 15
            },
            "average_waiting_time": 5
        }

        @mqtt_client.on_queues_changed_average_waiting_time()
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queues/changed-average-waiting-time"
        self.simulate_mqtt_message(mqtt_client, topic, [payload])

        handler_mock.assert_called_once_with([QueueWithAverageWaitingTime(**payload)])

    def test_on_queues_changed_waiting_number_specific_queue(self, mqtt_client):
        """
        Test the on_queues_changed_waiting_number decorator for a specific queue ID.
        """
        handler_mock = Mock()
        payload = {
            "queue": {
                "id": 99,
                "tag": "B",
                "name": "VIP Queue"
            },
            "waiting_tickets": 10
        }

        @mqtt_client.on_queues_changed_waiting_number(queue_id=99)
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queues/changed-waiting-number"
        self.simulate_mqtt_message(mqtt_client, topic, [payload])

        handler_mock.assert_called_once_with(QueueWithWaitingTickets(**payload))

    def test_on_queues_changed_waiting_number_all_queues(self, mqtt_client):
        """
        Test the on_queues_changed_waiting_number decorator for all queues.
        """
        handler_mock = Mock()
        payload = {
            "queue": {
                "id": 99,
                "tag": "B",
                "name": "VIP Queue"
            },
            "waiting_tickets": 10
        }

        @mqtt_client.on_queues_changed_waiting_number()
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queues/changed-waiting-number"
        self.simulate_mqtt_message(mqtt_client, topic, [payload])

        handler_mock.assert_called_once_with([QueueWithWaitingTickets(**payload)])

    def test_on_queues_changed_average_waiting_time_invalid_queue(self, mqtt_client):
        """
        Test the on_queues_changed_average_waiting_time decorator with a non-matching queue ID.
        """
        handler_mock = Mock()
        payload = {
            "queue": {
                "id": 1,
                "tag": "C",
                "name": "Non-matching Queue"
            },
            "average_waiting_time": 10
        }

        @mqtt_client.on_queues_changed_average_waiting_time(queue_id=42)
        def handle(msg):
            handler_mock(msg)

        # Simulate MQTT message
        topic = "locations/1/queues/changed-average-waiting-time"
        self.simulate_mqtt_message(mqtt_client, topic, [payload])

        handler_mock.assert_called_once_with(None)
