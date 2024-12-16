import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, Mock, patch

from pyqube.events.clients import MQTTClient
from pyqube.events.exceptions import SubscriptionError


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
        self.client = MQTTClient(api_key=self.api_key, location_id=1)

    def test_initialization_with_correct_credentials(self):
        """Test that the client initializes with correct credentials"""
        self.mock_client.username_pw_set.assert_called_once_with(self.api_key, None)
        self.mock_client.ws_set_options.assert_called_once_with(path='/')
        self.mock_client.tls_set_context.assert_called_once()
        self.mock_client.tls_insecure_set.assert_called_once_with(False)

    def test_connect_to_broker(self):
        """Test that the client connects to the broker with correct URL and port"""
        self.mock_client.connect.assert_called_once_with(
            host=MQTTClient.DEFAULT_BROKER_URL, port=MQTTClient.DEFAULT_BROKER_PORT, keepalive=60
        )
        self.mock_client.loop_start.assert_called_once()

    def test_initialization_with_custom_broker_url_and_port(self):
        """Test that the client initializes with custom broker URL and port"""
        custom_broker_url = "custom.broker.url"
        custom_broker_port = 1883
        client = MQTTClient(
            api_key=self.api_key, broker_url=custom_broker_url, broker_port=custom_broker_port, location_id=1
        )

        self.assertEqual(client.broker_url, custom_broker_url)
        self.assertEqual(client.broker_port, custom_broker_port)

    def test_disconnect(self):
        """Test that disconnect stops the loop and disconnects from broker"""
        self.client.disconnect()
        self.mock_client.loop_stop.assert_called_once()
        self.mock_client.disconnect.assert_called_once()

    def test_subscribe_to_topic_registers_handler_and_subscribes(self):
        """Test that subscribe_to_topic registers a handler and subscribes to the topic"""
        topic = 'test/topic'
        handler = Mock()
        self.client.subscribe_to_topic(topic, handler)
        self.assertIn(topic, self.client.message_handlers)
        self.assertIn(handler, self.client.message_handlers[topic])
        self.mock_client.subscribe.assert_called_once_with(topic)

    def test_subscribe_to_topic_raises_subscription_error_on_failure(self):
        """Test that SubscriptionError is raised if subscribing to a topic fails"""
        self.mock_client.subscribe.side_effect = Exception("Subscribe failed")
        with self.assertRaises(SubscriptionError):
            self.client.subscribe_to_topic("test/topic", lambda payload: None)

    def test_unsubscribe_from_topic_removes_handler_and_unsubscribes(self):
        """Test that unsubscribe_from_topic removes the handler and unsubscribes from the topic"""
        topic = 'test/topic'
        handler = Mock()
        self.client.subscribe_to_topic(topic, handler)
        self.client.unsubscribe_from_topic(topic)
        self.assertNotIn(topic, self.client.message_handlers)
        self.assertNotIn(topic, self.client._subscribed_topics)
        self.mock_client.unsubscribe.assert_called_once_with(topic)

    def test_unsubscribe_from_topic_raises_subscription_error_on_failure(self):
        """Test that SubscriptionError is raised if unsubscribing from a topic fails"""
        topic = 'test/topic'
        handler = Mock()
        self.client.subscribe_to_topic(topic, handler)
        self.mock_client.unsubscribe.side_effect = Exception("Unsubscribe failed")
        with self.assertRaises(SubscriptionError):
            self.client.unsubscribe_from_topic(topic)

    def test_list_subscribed_topics_returns_correct_list(self):
        """Test that list_subscribed_topics returns the correct list of subscribed topics"""
        topics = ['test/topic1', 'test/topic2']
        for topic in topics:
            self.client.subscribe_to_topic(topic, lambda payload: None)
        self.assertEqual(set(self.client.list_subscribed_topics()), set(topics))

    def test_age_calculation(self):
        """Test that age returns the correct number of days"""
        self.client._created_at = datetime.now(UTC) - timedelta(days=5)
        self.assertEqual(self.client.age(), 5)
