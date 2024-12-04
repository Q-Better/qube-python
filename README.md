# qube-python

Qube SDK is a Python library designed for seamless interaction with the Qube REST API and MQTT services. This SDK simplifies ticket and queue management while providing an easy-to-use interface for developers.

## Installation

You can install the SDK using [Poetry](https://python-poetry.org/):

```bash
poetry add qube-python
```

## Example Usage

### Events

Here is a brief example of how you can use the SDK to interact with the Qube MQTT Events:

```python
import time
from qube.events.clients import MQTTClient
from qube.events.types import Ticket

mqtt_client = MQTTClient(
    api_key="your_api_key_here",
    location_id=1
)

@mqtt_client.on_ticket_generated()
def handle_generated_ticket(ticket: Ticket):
    print(f"Generated ticket: {ticket}")

print("Listening for events. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    mqtt_client.disconnect()
```
For more detailed examples, check the [examples/events_example.py](examples/events_example.py) file.

### Rest

Here is a brief example of how you can use the SDK to interact with the Qube API:

```python
from qube.rest.clients import RestClient


def generate_ticket_for_each_queue(rest_client):
    pages_with_queues = rest_client.get_queue_management_manager().list_queues()
    # pages_with_queues is a generator object and it will make requests lazy
    for page in pages_with_queues:
        # each item is a page with multiple queues
        for queue in page:
            rest_client.get_queue_management_manager().set_queue_status(queue.id, True)
            generated_ticket = rest_client.get_queue_management_manager().generate_ticket(queue.id, False)
            print(generated_ticket)


if __name__ == '__main__':
    rest_client = RestClient(api_key="your_api_key_here", location_id=1)
    generate_ticket_for_each_queue(rest_client)

```
For more detailed examples, check the [examples/rest_example.py](examples/rest_example.py) file.
