class RestClientError(Exception):
    """Base class for all MQTT client-related errors."""
    pass


class BadRequest(RestClientError):
    """Raised when a client makes a request with some error."""
    pass


class NotAuthorized(RestClientError):
    """Raised when a client is not authorized to make a request."""
    pass


class Forbidden(RestClientError):
    """Raised when a client has not permission to make a request."""
    pass


class NotFound(RestClientError):
    """Raised when a client makes a request about something that doesn't exist."""
    pass
