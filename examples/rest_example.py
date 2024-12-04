import os

from qube.rest.clients import RestClient

# Retrieve environment variables
API_KEY = os.environ.get("QUBE_API_KEY")
LOCATION_ID = int(os.environ.get("QUBE_LOCATION_ID", 1))  # Default to 1 if not set

if not API_KEY:
    raise ValueError("Environment variable QUBE_API_KEY is required.")


def example():
    """
    Example usage of the Qube Rest SDK.
    """
    # Initialize the Rest client
    rest_client = RestClient(api_key=API_KEY, location_id=LOCATION_ID)

    location_access_id = 1
    counter_id = 1
    location_access_with_counter = rest_client.get_queue_management_manager().set_current_counter(
        location_access_id, counter_id
    )
    print(f"LocationAccess with current Counter: {location_access_with_counter}")

    queue_id = 1
    generated_ticket = rest_client.get_queue_management_manager().generate_ticket(queue_id, False)
    print(f"Generated Ticket: {generated_ticket}")

    profile_id = 1
    answering = rest_client.get_queue_management_manager().call_next_ticket_ending_current(profile_id)
    print(f"Answering: {answering}")

    current_answering = rest_client.get_queue_management_manager().get_current_answering(profile_id)
    print(f"Current Answering: {current_answering}")

    profile_id = 1
    ended_answering = rest_client.get_queue_management_manager().end_answering(profile_id, current_answering.id)
    print(f"Ended Answering: {ended_answering}")

    queue_id = 1
    queue = rest_client.get_queue_management_manager().set_queue_status(queue_id, True)
    print(f"Queue with status changed: {queue}")

    pages_with_queues = rest_client.get_queue_management_manager().list_queues()
    # pages_with_queues is a generator object and it will make requests lazy
    for page in pages_with_queues:
        # each item is a page with multiple queues
        for queue in page:
            print(f"Queue: {queue}")

    queues_list_id = 1
    pages_with_queues_of_queues_list = rest_client.get_queue_management_manager(
    ).list_queues_of_queues_list(queues_list_id)
    # pages_with_queues is a generator object and it will make requests lazy
    for page in pages_with_queues_of_queues_list:
        # each item is a page with multiple queues
        for queue in page:
            print(f"Queue of QueuesList: {queue}")


if __name__ == "__main__":
    example()
