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


class QueueManagementError(RestClientError):
    """Base class for Queue Management errors."""


class AlreadyAnsweringException(QueueManagementError):
    """Raised when a client is already answering and cannot make the request."""

    def __init__(self):
        self.message = "Already answering a Ticket."
        super().__init__(self.message)


class NoCurrentCounterException(QueueManagementError):
    """Raised when a client does not have the current counter in the location provided in request."""

    def __init__(self):
        self.message = "This Profile does not have a current_counter in this Location."
        super().__init__(self.message)


class InactiveCounterException(QueueManagementError):
    """Raised when a client has an associated Counter inactive."""

    def __init__(self):
        self.message = "The Counter that you are in is inactive."
        super().__init__(self.message)


class NoAccessToCounterException(QueueManagementError):
    """Raised when a client has no access to Counter."""

    def __init__(self):
        self.message = "This Profile is not associated to this Counter."
        super().__init__(self.message)
