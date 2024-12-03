from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


class StateEnum:
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
    state: StateEnum
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
    ticket: int
    profile: int
    counter: int
    queue: int
    local_runner: Optional[int]
    transferred_from_answering: Optional[int]
