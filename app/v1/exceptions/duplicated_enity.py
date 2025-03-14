from enums.status_codes import StatusCode
from app.v1.exceptions.service_error import ServiceError

class DuplicatedEntity(ServiceError):
    def __init__(self, db, collection, value):
        self.status = StatusCode.BAD_REQUEST
        self.detail = f"Entity on db {db} and collection {collection} with value {value} already exists"