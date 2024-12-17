import unittest
from unittest.mock import ANY, MagicMock, Mock

from pyqube.events.handlers import QueueHandler
from pyqube.types import (
    QueueGeneralDetails,
    QueueWithAverageWaitingTime,
    QueueWithWaitingTickets,
)


class ConcreteQueueHandler(QueueHandler):

    def subscribe_to_topic(self, topic: str, handler: Mock):
        # Mock implementation to satisfy abstract class
        pass


class TestQueueHandler(unittest.TestCase):

    def setUp(self):
        self.handler = ConcreteQueueHandler()
        self.handler.location_id = 1  # dummy location ID

    def test_on_queues_changed_average_waiting_time(self):
        # Mock the add_mqtt_handler method to prevent actual MQTT handling
        self.handler.add_mqtt_handler = MagicMock(return_value="Handler registered")

        # Call the method with queue_id=5
        result = self.handler.on_queues_changed_average_waiting_time(queue_id=5)

        # Verify add_mqtt_handler is called with correct parameters
        self.handler.add_mqtt_handler.assert_called_once_with(
            "locations/1/queues/changed-average-waiting-time",
            [QueueWithAverageWaitingTime],
            ANY  # Filter function
        )

        # Extract the filter function passed to add_mqtt_handler
        filter_function = self.handler.add_mqtt_handler.call_args[0][2]

        # Test the filter function by calling it with mock data
        mock_data = [
            MagicMock(
                queue=QueueGeneralDetails(
                    id=5,
                    tag="primaryQueue",
                    name="Primary Service Queue",
                    kpi_wait_count=5,
                    kpi_wait_time=10,
                    kpi_service_time=15
                )
            ),  # This should match
            MagicMock(
                queue=QueueGeneralDetails(
                    id=6,
                    tag="primaryQueue",
                    name="Primary Service Queue",
                    kpi_wait_count=5,
                    kpi_wait_time=10,
                    kpi_service_time=15
                )
            ),  # This should not match
        ]

        # Apply the filter function to the mock data
        filtered_data = filter_function(mock_data)

        # Check if the filter function behaves as expected (only the item with id 5 should be returned)
        self.assertEqual(filtered_data, mock_data[0])

        # Check the result of the method
        self.assertEqual(result, "Handler registered")

    def test_on_queues_changed_waiting_number(self):
        # Mock the add_mqtt_handler method to prevent actual MQTT handling
        self.handler.add_mqtt_handler = MagicMock(return_value="Handler registered")

        # Call the method with queue_id=10
        result = self.handler.on_queues_changed_waiting_number(queue_id=10)

        # Verify add_mqtt_handler is called with correct parameters
        self.handler.add_mqtt_handler.assert_called_once_with(
            "locations/1/queues/changed-waiting-number",
            [QueueWithWaitingTickets],
            ANY  # Filter function
        )

        # Check the result of the method
        self.assertEqual(result, "Handler registered")

    def test_get_queue_filter(self):
        # Create a filter function for queue_id=3
        filter_func = self.handler._get_queue_filter(queue_id=2)

        queue1 = QueueGeneralDetails(
            id=1,
            tag="primaryQueue",
            name="Primary Service Queue",
            kpi_wait_count=5,
            kpi_wait_time=10,
            kpi_service_time=15
        )
        queue2 = QueueGeneralDetails(
            id=2,
            tag="secondaryQueue",
            name="Secondary Service Queue",
            kpi_wait_count=10,
            kpi_wait_time=20,
            kpi_service_time=25
        )

        result1 = QueueWithWaitingTickets(queue=queue1, waiting_tickets=5)
        result2 = QueueWithWaitingTickets(queue=queue2, waiting_tickets=10)

        results = [result1, result2]

        # Apply the filter function to the mock data
        filtered_results = filter_func(results)

        # Assert that only the item with id=2 is returned
        self.assertEqual(filtered_results, result2)
