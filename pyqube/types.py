from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


def convert_str_to_datetime(dt_str: str) -> datetime:
    """
    Converts a string to a datetime object
    Args:
        dt_str (str): String that represents a datetime.
    Returns:
        datetime: datetime object build through given string value.
    """
    try:
        if dt_str.endswith("Z"):
            # Handle format with 'Z' as UTC indicator
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            # Handle format with explicit timezone offset
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {dt_str}") from e


class InvalidatedBySystemEnum:
    INVALIDATE_RESET = 1


class AuthGroupEnum:
    ADMIN = 1
    SERVICE_MANAGER = 2
    STAFF_MEMBER = 3
    DEVICE = 4


class LocationAccessStatusEnum:
    STATUS_PENDING = 1
    STATUS_ACCEPTED = 2


class FinishReasonEnum:
    CANCEL = 1
    TRANSFER_QUEUE = 2
    TRANSFER_COUNTER = 3
    TRANSFER_PROFILE = 4
    PAUSE = 5
    END = 6


class TicketStateEnum:
    WAITING = 1
    IN_SERVICE = 2
    PAUSED = 3
    CANCELLED = 4
    END = 5


@dataclass
class Ticket:
    """
    Class with all attributes of Qube's Ticket
    """

    id: int
    signature: str
    updated_at: datetime
    number: int
    printed_tag: str
    printed_number: str
    note: Optional[str]
    priority: bool
    priority_level: int
    created_at: datetime
    state: TicketStateEnum
    invalidated_by_system: Optional[InvalidatedBySystemEnum]
    ticket_local_runner: Optional[int]
    queue: int
    queue_dest: int
    counter_dest: Optional[int]
    profile_dest: Optional[int]
    generated_by_ticket_kiosk: Optional[int]
    generated_by_profile: Optional[int]
    generated_by_totem: Optional[int]
    is_generated_by_api_key: Optional[bool]
    generated_by_api_key: Optional[int]
    local_runner: Optional[int]
    tags: List[str]

    def __post_init__(self):
        self.created_at = convert_str_to_datetime(self.created_at)
        self.updated_at = convert_str_to_datetime(self.updated_at)


@dataclass
class Answering:
    """
    Class with all attributes of Qube's Answering
    """
    id: int
    created_at: str
    updated_at: str
    finish_reason: Optional[FinishReasonEnum]
    started_at: str
    finished_at: str
    invalidated_by_system: Optional[InvalidatedBySystemEnum]
    waiting_time: Optional[int]
    service_time: Optional[int]
    answering_local_runner: Optional[int]
    ticket: Ticket
    profile: int
    counter: int
    queue: int
    local_runner: Optional[int]
    transferred_from_answering: Optional[int]


@dataclass
class AnsweringTicket:
    """
    Represents a ticket that is being called in a queue or counter.
    """
    id: int
    answering: int
    priority: bool
    printed_tag: str
    printed_number: str
    number: int
    queue: int
    counter: int
    queue_tag: str
    counter_tag: str
    created_at: datetime
    tags: Optional[List[str]] = None


@dataclass
class QueuingSystemReset:
    """
    Represents a reset of the queuing system.
    """
    id: int
    location: int
    created_at: datetime
    updated_at: Optional[datetime] = None


@dataclass
class QueueGeneralDetails:
    """
    Represents the general details of a queue.
    """
    id: int
    tag: str
    name: str
    kpi_wait_count: Optional[int] = None
    kpi_wait_time: Optional[int] = None
    kpi_service_time: Optional[int] = None


@dataclass
class QueueWithAverageWaitingTime:
    """
    Represents a Queue with an associated average waiting time.
    """

    def __init__(self, queue, average_waiting_time):
        self.queue = queue if isinstance(queue, QueueGeneralDetails) else QueueGeneralDetails(**queue)
        self.average_waiting_time = average_waiting_time

    queue: QueueGeneralDetails
    average_waiting_time: int


@dataclass
class QueueWithWaitingTickets:
    """
    Represents a Queue with an associated waiting ticket.
    """

    def __init__(self, queue, waiting_tickets):
        self.queue = queue if isinstance(queue, QueueGeneralDetails) else QueueGeneralDetails(**queue)
        self.waiting_tickets = waiting_tickets

    queue: QueueGeneralDetails
    waiting_tickets: int


@dataclass
class Counter:
    """
    Class with some attributes of Qube's Counter. This class is used as nested object in other classes.
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    tag: str
    name: str
    location: int

    def __post_init__(self):
        self.created_at = convert_str_to_datetime(self.created_at)
        self.updated_at = convert_str_to_datetime(self.updated_at)
        if self.deleted_at:
            self.deleted_at = convert_str_to_datetime(self.deleted_at)


@dataclass
class LocationAccessWithCurrentCounter:
    """
    Class with all attributes of Qube's LocationAccess with an extra field (current_counter)
    """

    id: int
    location: int
    profile: int
    current_counter: Counter
    groups: List[AuthGroupEnum]
    invitation_email: str
    status: LocationAccessStatusEnum
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


@dataclass
class Queue:
    """
    Class with all attributes of Qube's Queue
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    tag: str
    name: str
    allow_priority: bool
    ticket_range_enabled: bool
    min_ticket_number: int
    max_ticket_number: int
    ticket_tolerance_enabled: bool
    ticket_tolerance_number: int
    kpi_wait_count: int
    kpi_wait_time: int
    kpi_service_time: int
    location: int
    schedule: int

    def __post_init__(self):
        self.created_at = convert_str_to_datetime(self.created_at)
        self.updated_at = convert_str_to_datetime(self.updated_at)
        if self.deleted_at:
            self.deleted_at = convert_str_to_datetime(self.deleted_at)
