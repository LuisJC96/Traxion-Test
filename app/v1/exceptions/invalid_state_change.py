from enums.status_codes import StatusCode
from app.v1.exceptions.service_error import ServiceError

class InvalidStateChange(ServiceError):
    def __init__(self, origin_state, required_state):
        self.status = StatusCode.BAD_REQUEST
        self.detail = f"Unable to transition from {origin_state} to {required_state}."