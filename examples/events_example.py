import os
import time

from qube.events.clients import MQTTClient
from qube.events.types import Ticket, AnsweringTicket, QueueWithAverageWaitingTime, QueueWithWaitingTickets, \
    QueuingSystemReset

# Retrieve environment variables
API_KEY = os.environ.get("QUBE_API_KEY")
LOCATION_ID = int(os.environ.get("QUBE_LOCATION_ID", 1))  # Default to 1 if not set

if not API_KEY:
    raise ValueError("Environment variable QUBE_API_KEY is required.")


def example():
    """
    Example usage of the Qube Events SDK.
    """
    # Initialize the MQTT client
    mqtt_client = MQTTClient(api_key=API_KEY, location_id=LOCATION_ID)

    # Register event handlers
    @mqtt_client.on_ticket_called(counter_id=1)
    def handle_ticket_from_counter(ticket: AnsweringTicket):
        print(f"Received ticket from counter 1: {ticket}")

    @mqtt_client.on_ticket_called(queue_id=2)
    def handle_ticket_from_queue(ticket: AnsweringTicket):
        print(f"Received ticket from queue 2: {ticket}")

    @mqtt_client.on_ticket_generated()
    def handle_generated_ticket(ticket: Ticket):
        print(f"Generated ticket: {ticket}")

    @mqtt_client.on_queues_changed_waiting_number(queue_id=204)
    def handle_queue_waiting_number_change(queue: QueueWithWaitingTickets):
        print(f"Queue waiting number changed: {queue}")

    @mqtt_client.on_queues_changed_average_waiting_time()
    def handle_queue_waiting_time_change(queue: QueueWithAverageWaitingTime):
        print(f"Queue average waiting time changed: {queue}")

    @mqtt_client.on_queuing_system_resets_created()
    def handle_system_reset(reset: QueuingSystemReset):
        print(f"Queuing system reset detected: {reset}")

    # Start listening for events
    print("Listening for events. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        mqtt_client.disconnect()


if __name__ == "__main__":
    example()
