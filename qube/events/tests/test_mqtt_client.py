import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, Mock, patch

from qube.events.clients import MQTTClient
from qube.events.exceptions import MessageHandlingError, SubscriptionError


class TestMQTTClient(unittest.TestCase):

    def setUp(self):
        # Set up mock for the paho mqtt Client
        patcher = patch('paho.mqtt.client.Client')
        self.mock_client_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_client = self.mock_client_class.return_value
        self.api_key = 'testapikey'
        # Mock subscribe method to be tracked
        self.mock_client.subscribe = MagicMock()
        # Instantiate MQTTClient with mocked MQTT broker connection
        self.client = MQTTClient(api_key=self.api_key)

    def test_initialization_with_correct_credentials(self):
        """Test that the client initializes with correct credentials"""
        self.mock_client.username_pw_set.assert_called_once_with(self.api_key, None)
        self.mock_client.ws_set_options.assert_called_once_with(path='/')
        self.mock_client.tls_set_context.assert_called_once()
        self.mock_client.tls_insecure_set.assert_called_once_with(False)

    def test_connect_to_broker(self):
        """Test that the client connects to the broker with correct URL and port"""
        self.mock_client.connect.assert_called_once_with(
            host=MQTTClient.BROKER_URL, port=MQTTClient.BROKER_PORT, keepalive=60
        )
        self.mock_client.loop_start.assert_called_once()

    def test_disconnect(self):
        """Test that disconnect stops the loop and disconnects from broker"""
        self.client.disconnect()
        self.mock_client.loop_stop.assert_called_once()
        self.mock_client.disconnect.assert_called_once()

    def test_add_handler_registers_handler(self):
        """Test that add_handler registers a handler function for a topic"""

        def sample_handler(payload):
            pass

        topic = 'test/topic'
        self.client.add_handler(topic, sample_handler)
        self.assertIn(topic, self.client.message_handlers)
        self.assertEqual(self.client.message_handlers[topic], sample_handler)

    def test_add_handler_subscribes_immediately_if_connected(self):
        """Test that add_handler subscribes immediately if client is connected"""
        topic = 'test/topic'

        # Add handler and expect subscribe to be called
        self.client.add_handler(topic, lambda payload: None)

        # Assert that subscribe was called immediately with the correct topic
        self.mock_client.subscribe.assert_called_once_with(topic)

    def test_add_handler_subscription_error(self):
        """Test that SubscriptionError is raised if subscribing fails"""
        self.mock_client.subscribe.side_effect = Exception("Subscribe failed")
        with self.assertRaises(SubscriptionError):
            self.client.add_handler("test/topic", lambda payload: None)

    def test_on_connect_connection_error(self):
        """Test that ConnectionError is raised if connection is unsuccessful"""
        with self.assertRaises(ConnectionError):
            self.client._on_connect(self.mock_client, None, None, 1)

    def test_on_connect_subscription_error(self):
        """Test that SubscriptionError is raised if subscribing fails on connect"""
        topic = 'test/topic'
        self.client.add_handler(topic, lambda payload: None)
        self.mock_client.subscribe.side_effect = Exception("Subscribe failed")
        with self.assertRaises(SubscriptionError):
            self.client._on_connect(self.mock_client, None, None, 0)

    def test_on_message_dispatches_to_correct_handler(self):
        """Test that on_message dispatches the message to the correct handler"""
        topic = 'test/topic'
        payload_data = b"test message"
        handler = Mock()
        self.client.add_handler(topic, handler)

        msg = Mock()
        msg.topic = topic
        msg.payload = payload_data

        self.client._on_message(self.mock_client, None, msg)
        handler.assert_called_once_with(payload_data)

    def test_on_message_message_handling_error(self):
        """Test that MessageHandlingError is raised if a handler fails"""
        topic = 'test/topic'
        handler = Mock(side_effect=Exception("Handler error"))
        self.client.add_handler(topic, handler)

        msg = Mock()
        msg.topic = topic
        msg.payload = b"message"

        with self.assertRaises(MessageHandlingError):
            self.client._on_message(self.mock_client, None, msg)

    def test_age_calculation(self):
        """Test that age returns the correct number of days"""
        self.client._created_at = datetime.now(UTC) - timedelta(days=5)
        self.assertEqual(self.client.age(), 5)
