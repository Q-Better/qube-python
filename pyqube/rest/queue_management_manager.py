from requests import Response

import base64
from typing import Generator, List, Optional

from pyqube.rest.exceptions import (
    AlreadyAnsweringException,
    AnsweringAlreadyProcessedException,
    BadRequest,
    Forbidden,
    HasLocalRunnerException,
    InactiveCounterException,
    InactiveQueueException,
    InternalServerError,
    InvalidScheduleException,
    MismatchingCountersException,
    NoAccessToCounterException,
    NoCurrentCounterException,
    NotAuthorized,
    NotFound,
    PaymentRequired,
    TicketsLimitReachedException,
)
from pyqube.rest.graphql_generators import QueuesListGraphQLGenerator
from pyqube.types import (
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
    'inactive_queue': InactiveQueueException,
    'invalid_schedule': InvalidScheduleException,
    'tickets_limit_reached': TicketsLimitReachedException,
}

STATUS_CODE_TO_EXCEPTION = {
    400: BadRequest,
    401: NotAuthorized,
    402: PaymentRequired,
    403: Forbidden,
    404: NotFound,
    500: InternalServerError,
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
            InternalServerError: If API returns a InternalServerError exception.
            AlreadyAnsweringException: If API returns a AlreadyAnsweringException exception.
            NoCurrentCounterException: If API returns a NoCurrentCounterException exception.
            InactiveCounterException: If API returns a InactiveCounterException exception.
            NoAccessToCounterException: If API returns a NoAccessToCounterException exception.
            AnsweringAlreadyProcessedException: If API returns a AnsweringAlreadyProcessedException exception.
            MismatchingCountersException: If API returns a MismatchingCountersException exception.
            HasLocalRunnerException: If API returns a HasLocalRunnerException exception.
            InactiveQueueException: If API returns a InactiveQueueException exception.
            InvalidScheduleException: If API returns a InvalidScheduleException exception.
            TicketsLimitReachedException: If API returns a TicketsLimitReachedException exception.
        """
        if response.status_code == 400 or response.status_code == 404:
            try:
                response_data = response.json()
                sub_type_exception = SUB_TYPE_TO_EXCEPTION.get(response_data.get("sub_type"))
                if sub_type_exception:
                    raise sub_type_exception
            except ValueError:
                pass
        exception = STATUS_CODE_TO_EXCEPTION.get(response.status_code)
        if exception:
            raise exception

    def generate_ticket(self, queue: int, priority: bool) -> Ticket:
        """
        Generate a ticket for a given queue with priority or not.
        Args:
            queue (int): Queue's id that will be generated the ticket.
            priority (bool): Boolean that defines if Ticket is priority or not.
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

    def call_next_ticket_ending_current(self, profile_id: int) -> Answering:
        """
        Call the next ticket.
        Args:
            profile_id (int): Profile's id that calls the ticket.
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

    def get_current_answering(self, profile_id: int) -> Optional[Answering]:
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

        if response.content.strip():
            return Answering(**response.json())
        else:
            return None

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

    def list_queues(self, page_size: int = 10) -> Generator[List[Queue], None, None]:
        """
        Lazily fetches queues from the API.
        List queues using `yield` for efficient processing of paginated API responses.
        This method retrieves and yields items one at a time, reducing memory usage and
        improving performance for large datasets.
        Args:
            page_size (int): Number of Queues per page.
        Returns:
            Generator[List[Queue]]: Generator that will iterate over pages of Queues.
        """
        has_next_page = True
        page = 1
        while has_next_page:
            params = {
                "page": page,
                "page_size": page_size
            }
            response = self.client.get_request(f"/locations/{self.client.location_id}/queues/", params=params)
            self._validate_response(response)

            response_data = response.json()

            if response_data.get("next"):
                page += 1
            else:
                has_next_page = False

            yield [Queue(**item) for item in response_data["results"]]

    def list_queues_of_queues_list(self, queues_list_id: int, page_size: int = 10) -> List[Queue]:
        """
        Gets one list of queues that are associated with given QueuesList
        Args:
            queues_list_id (int): QueuesList's id that have queues associated.
            page_size (int): Number of Queues per page.
        Returns:
            List[Queue]: List of Queues associated with given QueuesList.
        """
        has_next_page = True
        after = "\"\""

        while has_next_page:
            list_of_queues_objects = list()

            query = QueuesListGraphQLGenerator.generate_query_body(
                queues_list=queues_list_id, first=page_size, after=after
            )

            response = self.client.make_graphql_request(query)
            self._validate_response(response)

            response_data = response.json()

            list_of_queues = [edge["node"]["queue"] for edge in response_data["data"]["queues_lists_queues"]["edges"]]

            for queue in list_of_queues:
                queue["id"] = int(base64.b64decode(queue["id"]).decode('utf-8').split(":")[1])
                queue["location"] = int(base64.b64decode(queue["location"]["id"]).decode('utf-8').split(":")[1])
                if queue.get("schedule"):
                    queue["schedule"] = int(base64.b64decode(queue["schedule"]["id"]).decode('utf-8').split(":")[1])
                list_of_queues_objects.append(Queue(**queue))

            if response_data['data']['queues_lists_queues']['pageInfo']['hasNextPage']:
                after = f"\"{response_data['data']['queues_lists_queues']['pageInfo']['endCursor']}\""
            else:
                has_next_page = False

            yield list_of_queues_objects
