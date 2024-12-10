# qube-python

Qube SDK is a Python library designed for seamless interaction with the Qube REST API and MQTT services. This SDK simplifies ticket and queue management while providing an easy-to-use interface for developers.

## Installation

You can install the SDK using [Poetry](https://python-poetry.org/):

```bash
poetry add qube-python
```

## Example Usage

Here’s a brief example demonstrating how you can use the Qube SDK to interact with both the Qube API and Event Handling:

### Events

```python
import time
from qube import QubeClient
from qube.types import Ticket


def main():
    qube_client = QubeClient(api_key="your_api_key_here", location_id=1)

    @qube_client.on_ticket_generated()
    def handle_generated_ticket(ticket: Ticket):
        print(f"Generated ticket: {ticket}")

    print("Listening for events. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        qube_client.disconnect()


if __name__ == "__main__":
    main()
```

### REST API

```python
from qube import QubeClient


def generate_ticket_for_each_queue(qube_client):
    pages_with_queues = qube_client.get_queue_management_manager().list_queues()
    # pages_with_queues is a list of pages, each page contains a list of queues
    for page in pages_with_queues:
        # each item is a page with multiple queues
        for queue in page:
            qube_client.get_queue_management_manager().set_queue_status(queue.id, True)
            generated_ticket = qube_client.get_queue_management_manager().generate_ticket(queue.id, False)
            print(generated_ticket)


if __name__ == '__main__':
    qube_client = QubeClient(api_key="your_api_key_here", location_id=1)
    generate_ticket_for_each_queue(qube_client)
```

Explore additional usage examples and detailed workflows in the [examples directory](examples/).
- **Event Handling Example:** [events_example.py](examples/events_example.py)  
- **REST API Example:** [rest_example.py](examples/rest_example.py)  


