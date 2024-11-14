from requests import Response

from qube.rest.exceptions import BadRequest, Forbidden, NotAuthorized, NotFound
from qube.rest.types import Ticket


ERROR_CODE_TO_EXCEPTION = {
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
        """
        exception = ERROR_CODE_TO_EXCEPTION.get(response.status_code)
        if exception is not None:
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
