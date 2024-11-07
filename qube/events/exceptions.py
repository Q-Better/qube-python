class MQTTClientError(Exception):
    """Base class for all MQTT client-related errors."""
    pass


class SubscriptionError(MQTTClientError):
    """Raised when there is an issue subscribing to a topic."""
    pass


class MessageHandlingError(MQTTClientError):
    """Raised when an error occurs while handling an MQTT message."""
    pass
