from enums.status_codes import StatusCode
from app.v1.exceptions.service_error import ServiceError

class EntityNotFound(ServiceError):
    def __init__(self, origin_state, required_state, possible_transitions):
        self.status_code = StatusCode.BAD_REQUEST
        self.details = (f"Unable to transition from {origin_state} to {required_state} "
                        f"The possible transitions are: {possible_transitions}")