class MQTTClientError(Exception):
    """Base class for all MQTT client-related errors."""
    pass


class SubscriptionError(MQTTClientError):
    """Raised when there is an issue subscribing to a topic."""
    pass


class MessageHandlingError(MQTTClientError):
    """Raised when an error occurs while handling an MQTT message."""
    pass


class PayloadError(MQTTClientError):
    """Base class for payload-related errors."""
    pass


class PayloadFormatError(PayloadError):
    """Raised when there is an issue with the format of the message payload."""
    pass


class PayloadTypeError(PayloadError):
    """Raised when the payload type does not match the expected type."""
    pass


class HandlerRegistrationError(MQTTClientError):
    """Raised when there is an issue registering an MQTT handler."""
    pass


class InvalidTicketHandlerArgumentsError(MQTTClientError):
    """Raised when both or neither 'queue_id' and 'counter_id' are provided."""
    pass
