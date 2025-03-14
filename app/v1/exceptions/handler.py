import json
from functools import wraps
from datetime import datetime
from fastapi import Request, Response
from enums.status_codes import StatusCode
from app.v1.exceptions.service_error import ServiceError


def exception_handler(response_status:StatusCode = StatusCode.OK):
    def wrapper(func):
        @wraps(func)
        async def wrapped_function(request:Request, response:Response, *args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                response.status_code = response_status.value
                response.body = json.dumps(await func(request, response, *args, **kwargs)).encode("utf-8")
            except ServiceError as error:
                response.status_code = error.status.value
                response.body = json.dumps({
                    "status_code":error.status.value,
                    "detail": error.detail,
                    "timestamp": timestamp,
                }).encode("utf-8")
            except Exception as error:
                response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value
                response.body  = json.dumps({
                    "status_code": StatusCode.INTERNAL_SERVER_ERROR.value,
                    "detail": str(error),
                    "timestamp": timestamp,
                }).encode("utf-8")
            return response
        return wrapped_function
    return wrapper
