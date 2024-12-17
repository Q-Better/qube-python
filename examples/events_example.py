import os
import time

from pyqube import QubeClient
from pyqube.types import (
    AnsweringTicket,
    QueueWithAverageWaitingTime,
    QueueWithWaitingTickets,
    QueuingSystemReset,
    Ticket,
)


# Retrieve required environment variables for API configuration
API_KEY = os.environ.get(
    "QUBE_API_KEY", "your_api_key_here"
)  # Replace with your API key if not using environment variables
LOCATION_ID = int(
    os.environ.get("QUBE_LOCATION_ID", 1)
)  # Replace with your Location ID if not using environment variables


def example():
    """
    Example usage of the Qube Events SDK.
    """
    # Initialize the QubeClient
    qube_client = QubeClient(api_key=API_KEY, location_id=LOCATION_ID)

    # Placeholder values for IDs. Update these with the actual IDs from your Qube account.
    # They are associated with the specified location ID.
    queue_id = 789  # Example queue ID
    counter_id = 456  # Example counter ID

    # Register event handlers
    @qube_client.on_ticket_called(counter_id=counter_id)
    def handle_ticket_from_counter(ticket: AnsweringTicket):
        print(f"Received ticket from counter {counter_id}: {ticket}")

    @qube_client.on_ticket_called(queue_id=queue_id)
    def handle_ticket_from_queue(ticket: AnsweringTicket):
        print(f"Received ticket from queue {queue_id}: {ticket}")

    @qube_client.on_ticket_generated()
    def handle_generated_ticket(ticket: Ticket):
        print(f"Generated ticket: {ticket}")

    @qube_client.on_queues_changed_waiting_number(queue_id=queue_id)
    def handle_queue_waiting_number_change(queue: QueueWithWaitingTickets):
        print(f"Queue waiting number changed: {queue}")

    @qube_client.on_queues_changed_average_waiting_time()
    def handle_queue_waiting_time_change(queue: QueueWithAverageWaitingTime):
        print(f"Queue average waiting time changed: {queue}")

    @qube_client.on_queuing_system_resets_created()
    def handle_system_reset(reset: QueuingSystemReset):
        print(f"Queuing system reset detected: {reset}")

    # Start listening for events
    print("Listening for events. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        qube_client.disconnect()


if __name__ == "__main__":
    example()
