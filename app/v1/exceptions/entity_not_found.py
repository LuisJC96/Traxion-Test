from enums.status_codes import StatusCode
from app.v1.exceptions.service_error import ServiceError

class EntityNotFound(ServiceError):
    def __init__(self, db, collection, filter):
        self.status = StatusCode.NOT_FOUND
        self.detail = f"Entity on db {db} and collection {collection} with filter {filter} Not Found"