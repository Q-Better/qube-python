import json
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, List, Optional, Type, Union

from pyqube.events.exceptions import (
    HandlerRegistrationError,
    InvalidTicketHandlerArgumentsError,
    PayloadFormatError,
    PayloadTypeError,
)
from pyqube.types import (
    AnsweringTicket,
    QueueWithAverageWaitingTime,
    QueueWithWaitingTickets,
    QueuingSystemReset,
    Ticket,
)


class MQTTEventHandlerBase(ABC):

    def __init__(self):
        self.message_handlers = None

    def add_mqtt_handler(
        self,
        topic: str,
        payload_type: Optional[Union[List[Type], Type]] = None,
        payload_filter: Optional[Callable] = None
    ):
        """
        Registers an MQTT handler for a given topic and message type.

        Args:
            topic (str): The MQTT topic to subscribe to.
            payload_type (Type or List[Type]): Expected data type for decoding the message payload.
                If a list type is specified, the payload is expected to be a list of dictionaries.
            payload_filter (Callable, optional): A function to filter the payload before passing it to the handler.
        """

        def decorator(func):

            @wraps(func)
            def wrapper(payload):
                msg = self._decode_payload(payload, payload_type)
                if msg is not None:
                    if payload_filter:
                        msg = payload_filter(msg)
                    return func(msg)

            # Check if the exact handler is already registered for the topic
            existing_handlers = self.message_handlers.get(topic, [])
            for existing_handler in existing_handlers:
                if getattr(existing_handler, '__wrapped__', None) == func:
                    raise HandlerRegistrationError(
                        f"Handler '{func.__name__}' is already registered for topic '{topic}'."
                    )

            try:
                # Register the handler
                self.subscribe_to_topic(topic, wrapper)
            except Exception as e:
                raise HandlerRegistrationError(f"Failed to register handler for topic '{topic}': {e}")

            return wrapper

        return decorator

    @staticmethod
    def _decode_payload(payload: bytes, payload_type: Union[Type, List[Type]]):
        """
        Decodes a JSON payload into a specified message type.

        Args:
            payload (bytes): The raw message payload.
            payload_type (Type or List[Type]): The type(s) to decode the payload into.

        Returns:
            An instance of the specified type or a list of instances if the payload_type is a list.
            None if decoding fails.
        """
        try:
            data = json.loads(payload.decode('utf-8'))

            # Check if we expect a list of items
            if isinstance(payload_type, list) and payload_type:
                item_type = payload_type[0]
                if isinstance(data, list):
                    return [item_type(**item) for item in data]
                else:
                    raise PayloadFormatError("Expected payload to be a list of dictionaries.")

            # For a single item
            return payload_type(**data)
        except json.JSONDecodeError as e:
            raise PayloadFormatError("Invalid JSON payload.") from e
        except TypeError as e:
            raise PayloadTypeError(f"Type mismatch in payload for type '{payload_type}': {e}") from e

    @abstractmethod
    def subscribe_to_topic(self, topic: str, handler) -> None:
        pass


class QueuingSystemResetHandler(MQTTEventHandlerBase, ABC):
    """
    Handles MQTT events related to queuing system resets.
    """

    def __init__(self):
        super().__init__()
        self.location_id = None

    def on_queuing_system_resets_created(self):
        """
        Registers a handler for the 'created' event of queuing system resets.

        Returns:
            The decorator for the handler function.
        """
        topic = f"locations/{self.location_id}/queuing-system-resets/created"
        return self.add_mqtt_handler(topic, QueuingSystemReset)


class QueueHandler(MQTTEventHandlerBase, ABC):
    """
    Handles MQTT events related to queues.
    """

    def __init__(self):
        super().__init__()
        self.location_id = None

    def on_queues_changed_average_waiting_time(self, queue_id: Optional[int] = None):
        """
        Registers a handler for the 'changed average waiting time' event of queues.

        Args:
            queue_id (Optional[int]): The ID of the queue to filter events for. If not provided, all queues are handled.

        Returns:
            The decorator for the handler function.
        """
        topic = f"locations/{self.location_id}/queues/changed-average-waiting-time"
        return self.add_mqtt_handler(topic, [QueueWithAverageWaitingTime], self._get_queue_filter(queue_id))

    def on_queues_changed_waiting_number(self, queue_id: Optional[int] = None):
        """
        Registers a handler for the 'changed waiting number' event of queues.

        Args:
            queue_id (Optional[int]): The ID of the queue to filter events for. If not provided, all queues are handled.

        Returns:
            The decorator for the handler function.
        """
        topic = f"locations/{self.location_id}/queues/changed-waiting-number"
        return self.add_mqtt_handler(topic, [QueueWithWaitingTickets], self._get_queue_filter(queue_id))

    @staticmethod
    def _get_queue_filter(queue_id: Optional[int] = None):
        """
        Returns a filter function that filters results based on the provided queue_id.

        Args:
            queue_id (Optional[int]): The ID of the queue to filter by.

        Returns:
            A function that filters the results based on the queue_id.
        """

        def payload_filter(results):
            """Filters the payload based on queue_id, returning the matching item or all results."""
            if queue_id is not None:
                for result in results:
                    if result.queue.id == queue_id:
                        return result
                return None
            return results

        return payload_filter


class TicketHandler(MQTTEventHandlerBase, ABC):
    """
    Handles MQTT events related to tickets.
    """

    def __init__(self):
        super().__init__()
        self.location_id = None

    def on_ticket_generated(self):
        """
        Registers a handler for the 'generated' event of tickets.

        Returns:
            The decorator for the handler function.
        """
        topic = f"locations/{self.location_id}/tickets/generated"
        return self.add_mqtt_handler(topic, Ticket)

    def on_ticket_called(
        self,
        queue_id: Optional[int] = None,
        counter_id: Optional[int] = None,
    ):
        """
        Registers a handler for the 'called' event of tickets.

        Args:
            queue_id (int, optional): The ID of the queue to filter by.
            counter_id (int, optional): The ID of the counter to filter by.

        Returns:
            The decorator for the handler function.

        Raises:
            InvalidTicketHandlerArgumentsError: If both or neither `queue_id` and `counter_id` are provided.
        """
        # Check that exactly one of the arguments is provided
        if (queue_id is not None) and (counter_id is not None):
            raise InvalidTicketHandlerArgumentsError(
                "You can only provide one of 'queue_id' or 'counter_id', not both."
            )
        if (queue_id is None) and (counter_id is None):
            raise InvalidTicketHandlerArgumentsError("You must provide exactly one of 'queue_id' or 'counter_id'.")

        topic = f"locations/{self.location_id}"
        if queue_id is not None:
            topic += f"/queues/{queue_id}/tickets/called"
        else:
            topic += f"/counters/{counter_id}/tickets/called"

        return self.add_mqtt_handler(topic, AnsweringTicket)
