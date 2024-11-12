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
    Manager class that offers some methods about Queue management.
    """

    def __init__(self, client: object):
        self.client = client

    @classmethod
    def _validate_response(cls, response):
        """
        Internal method to validate response from server and raise an exception if there is something wrong.
        :param response: request's response
        """
        exception = ERROR_CODE_TO_EXCEPTION.get(response.status_code)
        if exception is not None:
            raise exception

    def generate_ticket(self, queue: int, priority: bool) -> Ticket:
        """
        Generate a ticket for a given queue with priority or not.
        :param queue: Queue's id for the ticket.
        :param priority: Boolean that defines if ticket is priority or not.
        :return: A ticket object.
        """
        data = {
            "queue": queue,
            "priority": priority
        }
        response = self.client.post_request(
            f"/locations/{self.client.location_id}/queue-management/tickets/generate/", data
        )

        self._validate_response(response)

        return Ticket(**response.json())
