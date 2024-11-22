from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union


class StateEnum:
    WAITING = 1
    IN_SERVICE = 2
    PAUSED = 3
    CANCELLED = 4
    END = 5


class InvalidatedBySystemEnum:
    INVALIDATE_RESET = 1


@dataclass
class Ticket:
    """
    Represents a ticket that has been generated.
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
    state: StateEnum
    invalidated_by_system: Optional[Union[InvalidatedBySystemEnum, None]]
    queue: int
    queue_dest: int
    ticket_local_runner: Optional[int] = None
    counter_dest: Optional[int] = None
    profile_dest: Optional[int] = None
    generated_by_ticket_kiosk: Optional[int] = None
    generated_by_profile: Optional[int] = None
    is_generated_by_api_key: Optional[bool] = None
    generated_by_api_key: Optional[int] = None
    local_runner: Optional[int] = None
    tags: List[str] = None


@dataclass
class QueuingSystemReset:
    """
    Represents a reset of the queuing system.
    """
    id: int
    location: int
    created_at: datetime
    updated_at: Optional[datetime] = None


from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
