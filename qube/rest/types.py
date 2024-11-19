from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


class TicketStateEnum:
    WAITING = 1
    IN_SERVICE = 2
    PAUSED = 3
    CANCELLED = 4
    END = 5


class FinishReasonEnum:
    CANCEL = 1
    TRANSFER_QUEUE = 2
    TRANSFER_COUNTER = 3
    TRANSFER_PROFILE = 4
    PAUSE = 5
    END = 6


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
    invalidated_by_system: Optional[Union[InvalidatedBySystemEnum, None]]
    ticket_local_runner: Optional[int]
    queue: int
    queue_dest: int
    counter_dest: Optional[int]
    profile_dest: Optional[int]
    generated_by_ticket_kiosk: Optional[int]
    generated_by_profile: Optional[int]
    is_generated_by_api_key: Optional[bool]
    generated_by_api_key: Optional[int]
    local_runner: Optional[int]
    tags: List[str]


@dataclass
class Answering:
    """
    Class with all attributes of Qube's Answering
    """
    id: int
    created_at: str
    updated_at: str
    finish_reason: Optional[Union[FinishReasonEnum, None]]
    started_at: str
    finished_at: str
    invalidated_by_system: Optional[Union[InvalidatedBySystemEnum, None]]
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
class Counter:
    """
    Class with some attributes of Qube's Counter. This class is used as nested object in other classes.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    tag: str
    name: str
    location: int


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
