import json
import pytest
from unittest.mock import Mock

from pyqube.events.clients import MQTTClient
from pyqube.events.exceptions import InvalidTicketHandlerArgumentsError
from pyqube.types import (
    AnsweringTicket,
    InvalidatedBySystemEnum,
    Ticket,
    TicketStateEnum,
)


class TestTicketHandlerDecorator:
    """
    Test suite for the TicketHandlerDecorator.
    """

    @pytest.fixture
    def mqtt_client(self):
        """
        Fixture to create an instance of MQTTClient.
        """
        return MQTTClient(api_key="dummy_api_key", location_id=1)

    def create_and_send_ticket(self, mqtt_client, handler, topic, id):
        """
        Helper method to create and send a ticket payload to the MQTT client.

        Args:
            mqtt_client (MQTTClient): The MQTT client instance.
            handler (Mock): The mock handler to be called.
            topic (str): The topic to which the message is sent.
            id (int): The ID to format the topic.
        """
        payload = AnsweringTicket(
            id=1,
            answering=2,
            priority=True,
            printed_tag="tag1",
            printed_number="001",
            number=101,
            tags=["urgent"],
            queue=1,
            counter=2,
            queue_tag="queue1",
            counter_tag="counter1",
            created_at='2024-01-01T00:00:00.000000Z'
        ).__dict__
        mqtt_client._on_message(
            mqtt_client.client, None, Mock(topic=topic.format(id), payload=json.dumps(payload).encode('utf-8'))
        )
        handler.assert_called_once_with(AnsweringTicket(**payload))

    def test_answering_ticket_handler_decorator_by_counter_id(self, mqtt_client):
        """
        Test that the handler is correctly registered and called for a specific counter ID.
        """
        handler = Mock()

        @mqtt_client.on_ticket_called(counter_id=124)
        def handle(msg):
            handler(msg)

        self.create_and_send_ticket(mqtt_client, handler, "locations/1/counters/{}/tickets/called", 124)

    def test_answering_ticket_handler_decorator_by_queue(self, mqtt_client):
        """
        Test that the handler is correctly registered and called for a specific queue ID.
        """
        handler = Mock()

        @mqtt_client.on_ticket_called(queue_id=90)
        def handle(msg):
            handler(msg)

        self.create_and_send_ticket(mqtt_client, handler, "locations/1/queues/{}/tickets/called", 90)

    def test_answering_ticket_handler_decorator_invalid_arguments(self, mqtt_client):
        """
        Test that providing both queue_id and counter_id raises an InvalidTicketHandlerArgumentsError.
        """
        with pytest.raises(InvalidTicketHandlerArgumentsError):

            @mqtt_client.on_ticket_called(queue_id=90, counter_id=124)
            def handle(msg):
                pass

    def test_on_ticket_generated(self, mqtt_client):
        """
        Test that the handler is correctly registered and called for ticket generated events.
        """
        handler = Mock()

        @mqtt_client.on_ticket_generated()
        def handle(msg):
            handler(msg)

        payload = {
            "id": 12345,
            "signature": "abcde12345signature",
            "number": 98765,
            "printed_tag": "VIP",
            "printed_number": "000123",
            "note": "This is a priority ticket.",
            "priority": True,
            "priority_level": 1,
            "updated_at": '2024-01-01T00:00:00.000000Z',
            "created_at": '2024-01-01T00:00:00.000000Z',
            "state": TicketStateEnum.END,
            "invalidated_by_system": InvalidatedBySystemEnum.INVALIDATE_RESET,
            "ticket_local_runner": 101,
            "queue": 5,
            "queue_dest": 7,
            "counter_dest": 2,
            "profile_dest": 3,
            "generated_by_ticket_kiosk": 99,
            "generated_by_profile": 88,
            "generated_by_totem": 77,
            "is_generated_by_api_key": True,
            "generated_by_api_key": 123456,
            "local_runner": 2001,
            "tags": ["urgent", "vip", "queue5"]
        }

        mqtt_client._on_message(
            mqtt_client.client, None,
            Mock(topic="locations/1/tickets/generated", payload=json.dumps(payload).encode('utf-8'))
        )
        handler.assert_called_once_with(Ticket(**payload))
