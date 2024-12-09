import os
import time

from qube import QubeClient
from qube.types import Ticket, AnsweringTicket, QueueWithAverageWaitingTime, QueueWithWaitingTickets, \
    QueuingSystemReset

# Retrieve environment variables
API_KEY = os.environ["QUBE_API_KEY"]
LOCATION_ID = int(os.environ["QUBE_LOCATION_ID"])
QUEUE_ID = int(os.environ["QUBE_QUEUE_ID"])
COUNTER_ID = int(os.environ["QUBE_COUNTER_ID"])


def example():
    """
    Example usage of the Qube Events SDK.
    """
    # Initialize the QubeClient
    qube_client = QubeClient(api_key=API_KEY, location_id=LOCATION_ID)

    # Register event handlers
    @qube_client.on_ticket_called(counter_id=COUNTER_ID)
    def handle_ticket_from_counter(ticket: AnsweringTicket):
        print(f"Received ticket from counter {COUNTER_ID}: {ticket}")

    @qube_client.on_ticket_called(queue_id=QUEUE_ID)
    def handle_ticket_from_queue(ticket: AnsweringTicket):
        print(f"Received ticket from queue {QUEUE_ID}: {ticket}")

    @qube_client.on_ticket_generated()
    def handle_generated_ticket(ticket: Ticket):
        print(f"Generated ticket: {ticket}")

    @qube_client.on_queues_changed_waiting_number(queue_id=QUEUE_ID)
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
