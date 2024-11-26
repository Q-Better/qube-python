from requests import Response

from typing import Generator, List

from qube.rest.exceptions import (
    AlreadyAnsweringException,
    AnsweringAlreadyProcessedException,
    BadRequest,
    Forbidden,
    HasLocalRunnerException,
    InactiveCounterException,
    InactiveQueueException,
    MismatchingCountersException,
    NoAccessToCounterException,
    NoCurrentCounterException,
    NotAuthorized,
    NotFound,
)
from qube.rest.types import (
    Answering,
    LocationAccessWithCurrentCounter,
    Queue,
    Ticket,
)


SUB_TYPE_TO_EXCEPTION = {
    'already_answering': AlreadyAnsweringException,
    'no_associated_counter': NoCurrentCounterException,
    'inactive_counter': InactiveCounterException,
    'counter_not_associated': NoAccessToCounterException,
    'already_processed': AnsweringAlreadyProcessedException,
    'mismatching_counters': MismatchingCountersException,
    'has_local_runner': HasLocalRunnerException,
    'inactive_queue': InactiveQueueException
}

STATUS_CODE_TO_EXCEPTION = {
    400: BadRequest,
    401: NotAuthorized,
    403: Forbidden,
    404: NotFound
}


class QueueManagementManager:
    """
    Manager class that offers some methods about Queue management to make requests to API Server through Rest Client.
    """

    def __init__(self, client: object):
        """
        Initializes and connects the Queue Management Manager.
        Args:
            client (RestClient): Client that will expose methods to make requests directly to API Server.
        """
        self.client = client

    @classmethod
    def _validate_response(cls, response: Response):
        """
        Internal method to validate response from server and raise an exception if there is something wrong.
        Args:
            response (Response): Request's returned response.
        Raises:
            BadRequest: If API returns a BadRequest exception.
            NotAuthorized: If API returns a NotAuthorized exception.
            Forbidden: If API returns a Forbidden exception.
            NotFound: If API returns a NotFound exception.
            AlreadyAnsweringException: If API returns a AlreadyAnsweringException exception.
            NoCurrentCounterException: If API returns a NoCurrentCounterException exception.
            InactiveCounterException: If API returns a InactiveCounterException exception.
        """
        if response.status_code == 400:
            response_data = response.json()
            sub_type_exception = SUB_TYPE_TO_EXCEPTION.get(response_data.get("sub_type"))
            if sub_type_exception:
                raise sub_type_exception

        exception = STATUS_CODE_TO_EXCEPTION.get(response.status_code)
        if exception:
            raise exception

    def generate_ticket(self, queue: int, priority: bool) -> Ticket:
        """
        Generate a ticket for a given queue with priority or not.
        Args:
            queue (int): Path of URL to be added to base url to make the request.
            priority (bool): Query parameters that will be included in the URL.
        Returns:
            Ticket: The generated Ticket object.
        """
        data = {
            "queue": queue,
            "priority": priority
        }
        response = self.client.post_request(
            f"/locations/{self.client.location_id}/queue-management/tickets/generate/", data=data
        )

        self._validate_response(response)

        return Ticket(**response.json())

    def call_next_ticket(self, profile_id: int) -> Answering:
        """
        Call the next ticket.
        Args:
            profile_id (int): Profile's id that is call the ticket.
        Returns:
            Answering: The created Answering object.
        """
        params = {
            "end_current": True
        }
        response = self.client.post_request(
            f"/locations/{self.client.location_id}/queue-management/profiles/{profile_id}/tickets/call-next/",
            params=params
        )
        self._validate_response(response)

        return Answering(**response.json())

    def set_current_counter(self, location_access_id: int, counter_id: int) -> LocationAccessWithCurrentCounter:
        """
        Set the current Counter on a given LocationAccess.
        Args:
            location_access_id (int): LocationAccess' id that will have stored the current counter information.
            counter_id (int): Counter's id that will be setted.
        Returns:
            LocationAccessWithCurrentCounter: The updated LocationAccess object.
        """
        data = {
            "counter": counter_id
        }
        response = self.client.put_request(
            f"/locations/{self.client.location_id}/location-accesses/{location_access_id}/associate-counter/",
            data=data
        )
        self._validate_response(response)

        return LocationAccessWithCurrentCounter(**response.json())

    def end_answering(self, profile_id: int, answering_id: int) -> Answering:
        """
        Ends the given answering.
        Args:
            profile_id (int): Profile's id that is answering.
            answering_id (int): Answering's id that will be ended.
        Returns:
            Answering: The ended Answering object.
        """
        response = self.client.put_request(
            f"/locations/{self.client.location_id}/queue-management/profiles/{profile_id}/answerings/{answering_id}/end/"
        )
        self._validate_response(response)

        return Answering(**response.json())

    def get_current_answering(self, profile_id: int) -> Answering:
        """
        Gets the current answering of given profile.
        Args:
            profile_id (int): Profile's id that is answering.
        Returns:
            Answering: The current Answering object.
        """
        response = self.client.get_request(
            f"/locations/{self.client.location_id}/queue-management/profiles/{profile_id}/answerings/current/"
        )
        self._validate_response(response)

        return Answering(**response.json())

    def set_queue_status(self, queue_id: int, is_active: bool) -> Queue:
        """
        Sets the status of given queue.
        Args:
            queue_id (int): Queue's id that will have status changed.
            is_active (bool): Value to set in Queue.
        Returns:
            Queue: The updated Queue object.
        """
        data = {
            "is_active": is_active
        }
        response = self.client.put_request(f"/locations/{self.client.location_id}/queues/{queue_id}/status/", data=data)
        self._validate_response(response)

        return Queue(**response.json())

    def list_queues(self) -> Generator[List[Queue], None, None]:
        """
        Lazily fetches queues from the API.
        List queues using `yield` for efficient processing of paginated API responses.
        This method retrieves and yields items one at a time, reducing memory usage and
        improving performance for large datasets.
        Returns:
            Generator[List[Queue]]: Generator that will iterate over pages of Queues.
        """
        has_next_page = True
        page = 1
        while has_next_page:
            params = {
                "page": page,
            }
            response = self.client.get_request(f"/locations/{self.client.location_id}/queues/", params=params)
            self._validate_response(response)

            response_data = response.json()
            yield [Queue(**item) for item in response_data["results"]]

            if response_data.get("next"):
                page += 1
            else:
                has_next_page = False
