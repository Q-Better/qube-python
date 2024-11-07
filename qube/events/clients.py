import paho.mqtt.client as mqtt
from datetime import UTC, datetime
from typing import Callable, Dict, Optional

from qube.events.exceptions import MessageHandlingError, SubscriptionError


class MQTTClient:
    """
    A versatile MQTT client for connecting to an MQTT broker, subscribing to topics,
    and handling message events with user-defined handlers.
    """

    BROKER_URL = "mqtt.dev.qube.q-better.com"
    BROKER_PORT = 8883

    def __init__(self, api_key: str):
        """
        Initializes and connects the MQTT client.

        Args:
            api_key (str): API key for client authentication.

        Raises:
            ConnectionError: If unable to connect to the broker.
        """

        self.client = mqtt.Client()
        self.message_handlers: Dict[str, Callable[[bytes], None]] = {}  # Maps topics to handler functions
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
            self.client.connect(host=self.BROKER_URL, port=self.BROKER_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MQTT broker at {self.BROKER_URL}:{self.BROKER_PORT}: {e}")

    def disconnect(self) -> None:
        """Stops the MQTT network loop and disconnects from the broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client: mqtt.Client, userdata: Optional[object], flags: dict, rc: int) -> None:
        """
        Callback triggered upon connecting to the MQTT broker. Subscribes to all topics
        that have registered handlers.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Optional[object]): Optional user data (not used).
            flags (dict): Response flags from the broker.
            rc (int): Connection result (0 indicates success).

        Raises:
            ConnectionError: If the client fails to connect successfully.
            SubscriptionError: If subscribing to any topic fails.
        """
        if rc == 0:
            for topic in self.message_handlers:
                try:
                    self.client.subscribe(topic)
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
        for topic, handler in self.message_handlers.items():
            if mqtt.topic_matches_sub(topic, msg.topic):
                try:
                    handler(msg.payload)
                except Exception as e:
                    raise MessageHandlingError(f"Error handling message for topic '{topic}': {e}")

    def add_handler(self, topic: str, handler: Callable[[bytes], None]) -> None:
        """
        Registers a handler function for a specific MQTT topic. If already connected,
        immediately subscribes to the topic.

        Args:
            topic (str): The MQTT topic to subscribe to.
            handler (Callable[[bytes], None]): A function that processes the message payload.

        Raises:
            SubscriptionError: If the subscription fails.
        """
        self.message_handlers[topic] = handler
        if self.client.is_connected():
            try:
                self.client.subscribe(topic)
            except Exception as e:
                raise SubscriptionError(f"Failed to subscribe to topic '{topic}': {e}")

    def age(self) -> int:
        """
        Calculates the age of the MQTTClient instance in days.

        Returns:
            int: Age in days since the client was created.
        """
        return (datetime.now(UTC) - self._created_at).days
