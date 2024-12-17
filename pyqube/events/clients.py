import paho.mqtt.client as mqtt
from datetime import UTC, datetime
from typing import Callable, Dict, Optional

from pyqube.events.exceptions import MessageHandlingError, SubscriptionError
from pyqube.events.handlers import (
    QueueHandler,
    QueuingSystemResetHandler,
    TicketHandler,
)


class MQTTClient(TicketHandler, QueuingSystemResetHandler, QueueHandler):
    """
    A versatile MQTT client for connecting to an MQTT broker, subscribing to topics,
    and handling message events with user-defined handlers.
    """

    DEFAULT_BROKER_URL = "mqtt.qube.q-better.com"
    DEFAULT_BROKER_PORT = 443

    def __init__(self, api_key: str, location_id: id, broker_url: str = None, broker_port: int = None):
        """
        Initializes and connects the MQTT client.

        Args:
            api_key (str): API key for client authentication.
            location_id (int): Location ID to use in requests.
            broker_url (str, optional): URL of the MQTT broker. Defaults to DEFAULT_BROKER_URL.
            broker_port (int, optional): Port of the MQTT broker. Defaults to DEFAULT_BROKER_PORT.
        Raises:
            ConnectionError: If unable to connect to the broker.
        """

        super().__init__()
        self.broker_url = broker_url or self.DEFAULT_BROKER_URL
        self.broker_port = broker_port or self.DEFAULT_BROKER_PORT
        self.location_id = location_id

        self.client = mqtt.Client()

        self.message_handlers: Dict[str, list[Callable[[bytes], None]]] = {}  # Maps topics to handler functions
        self._subscribed_topics = set()  # Tracks subscribed topics
        self._created_at = datetime.now(UTC)

        # Set the username for authentication
        self.client.username_pw_set(api_key, None)

        # Register internal event callbacks
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect

        # Configure WebSocket and TLS options for secure connection
        self.client.ws_set_options(path='/')
        self.client.tls_set_context()
        self.client.tls_insecure_set(False)

        # Connect to the MQTT broker
        self._connect_to_broker()

    def _connect_to_broker(self) -> None:
        """Connects to the MQTT broker and starts the network loop."""
        try:
            self.client.connect(host=self.broker_url, port=self.broker_port, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MQTT broker at {self.broker_url}:{self.broker_port}: {e}")

    def disconnect(self) -> None:
        """Stops the MQTT network loop and disconnects from the broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client: mqtt.Client, userdata: Optional[object], flags: dict, rc: int) -> None:
        """
        Callback triggered when the client successfully connects to the MQTT broker.
        Subscribes to all topics that have registered handlers.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Optional[object]): Optional user data (not used in this implementation).
            flags (dict): A dictionary of response flags from the broker.
            rc (int): The connection result code. A value of 0 indicates success, while any other value indicates failure.

        Raises:
            ConnectionError: If the connection to the broker fails (rc != 0).
            SubscriptionError: If subscribing to any topic fails after a successful connection.

        Notes:
            - The method subscribes to topics only if the connection is successful (rc == 0).
            - It attempts to subscribe to each topic stored in `_subscribed_topics` that has a registered handler.
        """
        if rc == 0:
            for topic in self._subscribed_topics:
                try:
                    if topic not in self.message_handlers:
                        client.subscribe(topic)
                except Exception as e:
                    raise SubscriptionError(f"Failed to subscribe to topic '{topic}': {e}")
        else:
            raise ConnectionError(f"Failed to connect to MQTT broker with return code {rc}")

    def _on_message(self, client: mqtt.Client, userdata: Optional[object], msg: mqtt.MQTTMessage) -> None:
        """
        Callback triggered when a message is received on a subscribed topic.
        Dispatches the message to the appropriate handler.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Optional[object]): Optional user data (not used).
            msg (mqtt.MQTTMessage): The received MQTT message.

        Raises:
            MessageHandlingError: If the handler for a topic fails.
        """
        for topic, handlers in self.message_handlers.items():
            if mqtt.topic_matches_sub(topic, msg.topic):
                for handler in handlers:
                    try:
                        handler(msg.payload)
                    except Exception as e:
                        raise MessageHandlingError(f"Error in handler for topic '{topic}': {e}")

    def subscribe_to_topic(self, topic: str, handler: Callable[[bytes], None]) -> None:
        """
        Subscribes to an MQTT topic and registers a handler function to process incoming messages.

        Args:
            topic (str): The MQTT topic to subscribe to.
            handler (Callable[[bytes], None]): A function that processes messages for this topic.
                It must accept a single argument of type `bytes` (the message payload).

        Raises:
            SubscriptionError: If subscribing to the topic fails.

        Notes:
            - The same handler will not be registered more than once for the same topic.
            - A topic is subscribed to only once, even if multiple handlers are added.
        """
        if topic not in self.message_handlers:
            self.message_handlers[topic] = []

        if handler not in self.message_handlers[topic]:
            self.message_handlers[topic].append(handler)
            if topic not in self._subscribed_topics:
                try:
                    self.client.subscribe(topic)
                    self._subscribed_topics.add(topic)
                except Exception as e:
                    raise SubscriptionError(f"Failed to subscribe to topic '{topic}': {e}")

    def unsubscribe_from_topic(self, topic: str) -> None:
        """
        Unsubscribes from an MQTT topic and removes its handler.
        """
        if topic in self._subscribed_topics:
            try:
                self.client.unsubscribe(topic)
                self._subscribed_topics.remove(topic)
                self.message_handlers.pop(topic, None)
            except Exception as e:
                raise SubscriptionError(f"Failed to unsubscribe from topic '{topic}': {e}")

    def list_subscribed_topics(self) -> list:
        """
        Lists all currently subscribed topics.
        """
        return list(self._subscribed_topics)

    def age(self) -> int:
        """
        Calculates the age of the MQTTClient instance in days.

        Returns:
            int: Age in days since the client was created.
        """
        return (datetime.now(UTC) - self._created_at).days
