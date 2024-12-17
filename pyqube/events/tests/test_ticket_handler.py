import pytest
from unittest.mock import Mock

from pyqube.events.exceptions import InvalidTicketHandlerArgumentsError
from pyqube.events.handlers import TicketHandler


# Concrete subclass for testing purposes
class ConcreteTicketHandler(TicketHandler):

    def subscribe_to_topic(self, topic: str, handler: Mock):
        pass


class TestTicketHandler:

    @pytest.fixture
    def ticket_handler(self):
        """Fixture to create a concrete instance of TicketHandler."""
        handler = ConcreteTicketHandler()
        handler.location_id = 1
        return handler

    def test_on_ticket_generated(self, ticket_handler):
        """Test that on_ticket_generated registers the correct handler."""
        handler = ticket_handler.on_ticket_generated()
        assert handler is not None

    def test_on_ticket_called_with_counter_id(self, ticket_handler):
        """Test that on_ticket_called registers the correct handler for counter_id."""
        handler = ticket_handler.on_ticket_called(counter_id=124)
        assert handler is not None

    def test_on_ticket_called_with_queue_id(self, ticket_handler):
        """Test that on_ticket_called registers the correct handler for queue_id."""
        handler = ticket_handler.on_ticket_called(queue_id=90)
        assert handler is not None

    def test_invalid_ticket_handler_arguments(self, ticket_handler):
        """Test the behavior when both queue_id and counter_id are provided."""
        with pytest.raises(InvalidTicketHandlerArgumentsError):
            ticket_handler.on_ticket_called(queue_id=90, counter_id=124)
