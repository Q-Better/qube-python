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


class InternalServerError(RestClientError):
    """Raised when a client makes a request and something is wrong with API Server."""
    pass


class PaymentRequired(RestClientError):
    """Raised when a client makes a request that requires payment."""
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


class AnsweringAlreadyProcessedException(QueueManagementError):
    """Raised when we are interacting with an answering that is already processed."""

    def __init__(self):
        self.message = "Answering is already processed and finished."
        super().__init__(self.message)


class MismatchingCountersException(QueueManagementError):
    """Raised when we are interacting with an answering that has a different counter from current counter."""

    def __init__(self):
        self.message = "The Counter of Answering is not the current_counter of Profile."
        super().__init__(self.message)


class InactiveQueueException(QueueManagementError):
    """Raised when we are interacting with an inactive Queue."""

    def __init__(self):
        self.message = "Queue is inactive."
        super().__init__(self.message)


class InvalidScheduleException(QueueManagementError):
    """Raised when we are generating a Ticket outside of the scheduled operating time."""

    def __init__(self):
        self.message = "You are currently outside the scheduled operating time. Please contact your admin."
        super().__init__(self.message)


class TicketsLimitReachedException(QueueManagementError):
    """Raised when we are generating a Ticket and Ticket limit was reached."""

    def __init__(self):
        self.message = "Tickets' limit was reached."
        super().__init__(self.message)


class LocalRunnerException(RestClientError):
    """Base class for Local Runner errors."""


class HasLocalRunnerException(LocalRunnerException):
    """Raised when we are interacting with an answering but there is a local runner associated."""

    def __init__(self):
        self.message = "This Location has Local Runner set: Queue Management action should be done through it."
        super().__init__(self.message)
