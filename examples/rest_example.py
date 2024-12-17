import os

from pyqube import QubeClient


# Retrieve required environment variables for API configuration
API_KEY = os.environ.get(
    "QUBE_API_KEY", "your_api_key_here"
)  # Replace with your API key if not using environment variables
LOCATION_ID = int(
    os.environ.get("QUBE_LOCATION_ID", 1)
)  # Replace with your Location ID if not using environment variables


def example():
    """
    Example usage of the Qube Rest SDK with placeholder values.
    """
    # Initialize the Rest client
    rest_client = QubeClient(api_key=API_KEY, location_id=LOCATION_ID)

    # Placeholder values for IDs. Update these with the actual IDs from your Qube account.
    # They are associated with the specified location ID.
    location_access_id = 123  # Example location access ID
    counter_id = 456  # Example counter ID
    queue_id = 789  # Example queue ID
    profile_id = 101  # Example profile ID
    queues_list_id = 202  # Example queues list ID

    # Set the current counter for a location access
    location_access_with_counter = rest_client.get_queue_management_manager().set_current_counter(
        location_access_id, counter_id
    )
    print(f"LocationAccess with current Counter: {location_access_with_counter}")

    # Generate a ticket for the queue
    generated_ticket = rest_client.get_queue_management_manager().generate_ticket(queue_id, False)
    print(f"Generated Ticket: {generated_ticket}")

    # Call the next ticket and end the current one
    answering = rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)
    print(f"Answering: {answering}")

    current_answering = rest_client.get_queue_management_manager().get_current_answering(profile_id)
    print(f"Current Answering: {current_answering}")

    ended_answering = rest_client.get_queue_management_manager().end_answering(profile_id, current_answering.id)
    print(f"Ended Answering: {ended_answering}")

    # Change the status of a queue
    queue = rest_client.get_queue_management_manager().set_queue_status(queue_id, True)
    print(f"Queue with status changed: {queue}")

    # List all queues
    pages_with_queues = rest_client.get_queue_management_manager().list_queues()
    for page in pages_with_queues:
        for queue in page:
            print(f"Queue: {queue}")

    # List all queues for a specific queues list
    pages_with_queues_of_queues_list = rest_client.get_queue_management_manager(
    ).list_queues_of_queues_list(queues_list_id)
    for page in pages_with_queues_of_queues_list:
        for queue in page:
            print(f"Queue of QueuesList: {queue}")


if __name__ == "__main__":
    example()
