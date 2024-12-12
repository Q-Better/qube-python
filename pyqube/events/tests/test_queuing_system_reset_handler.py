import unittest
from unittest.mock import MagicMock, Mock

from pyqube.events.handlers import QueuingSystemResetHandler
from pyqube.types import QueuingSystemReset


# Concrete subclass for testing purposes
class ConcreteQueuingSystemResetHandler(QueuingSystemResetHandler):

    def subscribe_to_topic(self, topic: str, handler: Mock):
        pass


class TestQueuingSystemResetHandler(unittest.TestCase):

    def setUp(self):
        self.handler = ConcreteQueuingSystemResetHandler()
        self.handler.location_id = 1  # dummy location ID

    def test_on_queuing_system_resets_created(self):
        # Mock the add_mqtt_handler method to prevent actual MQTT handling
        self.handler.add_mqtt_handler = MagicMock(return_value="Handler registered")

        result = self.handler.on_queuing_system_resets_created()

        self.handler.add_mqtt_handler.assert_called_once_with(
            "locations/1/queuing-system-resets/created", QueuingSystemReset
        )
        self.assertEqual(result, "Handler registered")
