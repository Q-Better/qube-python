import unittest
from unittest.mock import MagicMock

from pyqube.events.exceptions import (
    HandlerRegistrationError,
    PayloadFormatError,
    PayloadTypeError,
)
from pyqube.events.handlers import MQTTEventHandlerBase


class MockPayload:
    """
    A mock payload class for testing purposes.
    """

    def __init__(self, field1: str, field2: int):
        self.field1 = field1
        self.field2 = field2


class MockPayloadListItem:
    """
    A mock payload list item class for testing purposes.
    """

    def __init__(self, id: int):
        self.id = id


class TestMQTTEventHandlerBase(unittest.TestCase):
    """
    Unit tests for the MQTTEventHandlerBase class.
    """

    def setUp(self):

        class TestHandler(MQTTEventHandlerBase):
            """
            A test handler class inheriting from MQTTEventHandlerBase.
            """

            def __init__(self):
                super().__init__()
                self.message_handlers = {}

            def subscribe_to_topic(self, topic: str, handler) -> None:
                """
                Subscribe a handler to a specific topic.

                Args:
                    topic (str): The topic to subscribe to.
                    handler: The handler function to be called when a message is received on the topic.
                """
                if topic in self.message_handlers:
                    self.message_handlers[topic].append(handler)
                else:
                    self.message_handlers[topic] = [handler]

        self.handler = TestHandler()

    def test_add_handler_registers_handler(self):
        """
        Test that adding a handler registers it correctly.
        """

        def mock_handler(msg):
            pass

        self.handler.add_mqtt_handler("test/topic")(mock_handler)
        self.assertIn("test/topic", self.handler.message_handlers)
        self.assertEqual(len(self.handler.message_handlers["test/topic"]), 1)

    def test_add_handler_duplicate_registration_raises_error(self):
        """
        Test that adding a duplicate handler raises a HandlerRegistrationError.
        """

        def mock_handler(msg):
            pass

        self.handler.add_mqtt_handler("test/topic")(mock_handler)
        with self.assertRaises(HandlerRegistrationError):
            self.handler.add_mqtt_handler("test/topic")(mock_handler)

    def test_decode_payload_valid_data(self):
        """
        Test that decoding a valid payload returns the correct object.
        """
        payload = b'{"field1": "test", "field2": 123}'
        result = self.handler._decode_payload(payload, MockPayload)
        self.assertIsInstance(result, MockPayload)
        self.assertEqual(result.field1, "test")
        self.assertEqual(result.field2, 123)

    def test_decode_payload_invalid_json_raises_error(self):
        """
        Test that decoding an invalid JSON payload raises a PayloadFormatError.
        """
        payload = b'invalid-json'
        with self.assertRaises(PayloadFormatError):
            self.handler._decode_payload(payload, MockPayload)

    def test_decode_payload_type_mismatch_raises_error(self):
        """
        Test that decoding a payload with a type mismatch raises a PayloadTypeError.
        """
        payload = b'{"field1": "test", "field_unknown": "not-an-int"}'
        with self.assertRaises(PayloadTypeError):
            self.handler._decode_payload(payload, MockPayload)

    def test_decode_payload_list_valid_data(self):
        """
        Test that decoding a valid list payload returns the correct list of objects.
        """
        payload = b'[{"id": 1}, {"id": 2}]'
        result = self.handler._decode_payload(payload, [MockPayloadListItem])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)

    def test_decode_payload_list_invalid_data_raises_error(self):
        """
        Test that decoding an invalid list payload raises a PayloadFormatError.
        """
        payload = b'{"id": 1}'  # Not a list
        with self.assertRaises(PayloadFormatError):
            self.handler._decode_payload(payload, [MockPayloadListItem])

    def test_handler_executes_with_valid_payload(self):
        """
        Test that a handler executes correctly with a valid payload.
        """
        mock_handler = MagicMock()
        self.handler.add_mqtt_handler("test/topic", MockPayload)(mock_handler)
        payload = b'{"field1": "test", "field2": 123}'
        registered_handler = self.handler.message_handlers["test/topic"][0]
        registered_handler(payload)
        mock_handler.assert_called_once()
        mock_handler.assert_called_with(mock_handler.call_args[0][0])
        self.assertIsInstance(mock_handler.call_args[0][0], MockPayload)

    def test_handler_with_filter(self):
        """
        Test that a handler with a filter function processes the payload correctly.
        """

        def filter_func(payload):
            return {
                "field1": payload.field1.upper(),
                "field2": payload.field2
            }

        mock_handler = MagicMock()
        self.handler.add_mqtt_handler("test/topic", MockPayload, filter_func)(mock_handler)
        payload = b'{"field1": "test", "field2": 123}'
        registered_handler = self.handler.message_handlers["test/topic"][0]
        registered_handler(payload)
        mock_handler.assert_called_once()
        self.assertEqual(mock_handler.call_args[0][0].get('field1'), "TEST")
