from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


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

    def __init__(
        self,
        id: int,
        signature: str,
        number: int,
        printed_tag: str,
        printed_number: str,
        priority: bool,
        priority_level: int,
        created_at: str,
        state: TicketStateEnum,
        queue: int,
        queue_dest: int,
        tags: List[str],
        updated_at: str = None,
        deleted_at: str = None,
        note: str = None,
        invalidated_by_system: InvalidatedBySystemEnum = None,
        ticket_local_runner: int = None,
        counter_dest: int = None,
        profile_dest: int = None,
        generated_by_ticket_kiosk: int = None,
        generated_by_profile: int = None,
        generated_by_totem: int = None,
        is_generated_by_api_key: bool = None,
        generated_by_api_key: int = None,
        local_runner: int = None
    ):
        self.id = id
        self.signature = signature
        self.number = number
        self.printed_tag = printed_tag
        self.printed_number = printed_number
        self.priority = priority
        self.priority_level = priority_level
        self.state = state
        self.queue = queue
        self.queue_dest = queue_dest
        self.tags = tags
        self.created_at = convert_str_to_datetime(created_at)
        self.updated_at = convert_str_to_datetime(updated_at) if updated_at else None
        self.deleted_at = convert_str_to_datetime(deleted_at) if deleted_at else None
        self.note = note
        self.invalidated_by_system = invalidated_by_system
        self.ticket_local_runner = ticket_local_runner
        self.counter_dest = counter_dest
        self.profile_dest = profile_dest
        self.generated_by_ticket_kiosk = generated_by_ticket_kiosk
        self.generated_by_profile = generated_by_profile
        self.generated_by_totem = generated_by_totem
        self.is_generated_by_api_key = is_generated_by_api_key
        self.generated_by_api_key = generated_by_api_key
        self.local_runner = local_runner

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
class Counter:
    """
    Class with some attributes of Qube's Counter. This class is used as nested object in other classes.
    """

    def __init__(
        self,
        id: int,
        is_active: bool,
        created_at: str,
        tag: str,
        name: str,
        location: int,
        updated_at: str = None,
        deleted_at: str = None
    ):
        self.id = id
        self.is_active = is_active
        self.created_at = convert_str_to_datetime(created_at)
        self.tag = tag
        self.name = name
        self.location = location
        self.updated_at = convert_str_to_datetime(updated_at) if updated_at else None
        self.deleted_at = convert_str_to_datetime(deleted_at) if deleted_at else None

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

    def __init__(
        self,
        id: int,
        location: int,
        profile: int,
        current_counter: Counter,
        groups: List[AuthGroupEnum],
        invitation_email: str,
        status: LocationAccessStatusEnum,
        created_at: str,
        updated_at: str = None,
        deleted_at: str = None
    ):
        self.id = id
        self.location = location
        self.profile = profile
        self.current_counter = current_counter
        self.groups = groups
        self.invitation_email = invitation_email
        self.status = status
        self.created_at = convert_str_to_datetime(created_at)
        self.updated_at = convert_str_to_datetime(updated_at) if updated_at else None
        self.deleted_at = convert_str_to_datetime(deleted_at) if deleted_at else None

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

    def __init__(
        self,
        id: int,
        is_active: bool,
        created_at: str,
        tag: str,
        name: str,
        allow_priority: bool,
        ticket_range_enabled: bool,
        min_ticket_number: int,
        max_ticket_number: int,
        ticket_tolerance_enabled: bool,
        ticket_tolerance_number: int,
        kpi_wait_count: int,
        kpi_wait_time: int,
        kpi_service_time: int,
        location: int,
        schedule: int,
        updated_at: str = None,
        deleted_at: str = None,
    ):
        self.id = id
        self.is_active = is_active
        self.created_at = convert_str_to_datetime(created_at)
        self.updated_at = convert_str_to_datetime(updated_at) if updated_at else None
        self.deleted_at = convert_str_to_datetime(deleted_at) if deleted_at else None
        self.tag = tag
        self.name = name
        self.allow_priority = allow_priority
        self.ticket_range_enabled = ticket_range_enabled
        self.min_ticket_number = min_ticket_number
        self.max_ticket_number = max_ticket_number
        self.ticket_tolerance_enabled = ticket_tolerance_enabled
        self.ticket_tolerance_number = ticket_tolerance_number
        self.kpi_wait_count = kpi_wait_count
        self.kpi_wait_time = kpi_wait_time
        self.kpi_service_time = kpi_service_time
        self.location = location
        self.schedule = schedule

    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
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
