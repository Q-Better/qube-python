from dataclasses import dataclass


@dataclass
class Ticket:
    """
    Class with all attributes of Qube's Ticket
    """
    id: int
    signature: str
    number: int
    printed_number: str
    printed_tag: str
    queue: int
    queue_dest: int
    counter_dest: int
    profile_dest: int
    state: int
    generated_by_ticket_kiosk: int
    generated_by_profile: int
    generated_by_api_key: int
    priority: bool
    priority_level: int
    note: str
    updated_at: str
    created_at: str
    is_generated_by_api_key: bool
    invalidated_by_system: int
    ticket_local_runner: int
    tags: list
    local_runner: int
