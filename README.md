# qube-python

Qube SDK is a Python library designed for seamless interaction with the Qube REST API and MQTT services. This SDK simplifies ticket and queue management while providing an easy-to-use interface for developers.

## Installation

You can install the SDK using [Poetry](https://python-poetry.org/):

```bash
poetry add qube-python
```

## Example Usage

### Events

Here is a brief example of how you can use the SDK to interact with the Qube API:

```python
import time
from qube import QubeClient
from qube.types import Ticket

mqtt_client = QubeClient(
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

