from enums.status_codes import StatusCode

class ServiceError(Exception):
    def __init__(self, status: StatusCode, detail:str):
        self.status = status
        self.detail = detail
