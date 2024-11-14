from requests import Response

from qube.rest.exceptions import (
    AlreadyAnsweringException,
    BadRequest,
    Forbidden,
    InactiveCounterException,
    NoCurrentCounterException,
    NotAuthorized,
    NotFound,
)
from qube.rest.types import Answering, Ticket


SUB_TYPE_TO_EXCEPTION = {
    'already_answering': AlreadyAnsweringException,
    'no_associated_counter': NoCurrentCounterException,
    'inactive_counter': InactiveCounterException
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
            Ticket: The generated ticket object.
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
            profile_id (int): Profile's id that is called the ticket.
        Returns:
            Answering: The created answering object.
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
