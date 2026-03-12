from enum import StrEnum
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.common.responses import error_response


class ErrorCode(StrEnum):
    AUTH_UNAUTHORIZED = "AUTH_UNAUTHORIZED"
    AUTH_INVALID_TOKEN = "AUTH_INVALID_TOKEN"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AppException(Exception):
    def __init__(self, *, code: ErrorCode, message_key: str, status_code: int, context: dict[str, Any] | None = None) -> None:
        super().__init__(message_key)
        self.code = code
        self.message_key = message_key
        self.status_code = status_code
        self.context = context or {}


async def app_exception_handler(_: Request, exc: AppException) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.status_code, content=error_response(code=exc.code.value, message_key=exc.message_key, details=exc.context))


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> ORJSONResponse:
    return ORJSONResponse(status_code=422, content=error_response(code=ErrorCode.VALIDATION_ERROR.value, message_key="errors.validation.invalid_request", details={"fields": exc.errors()}))


async def generic_exception_handler(_: Request, __: Exception) -> ORJSONResponse:
    return ORJSONResponse(status_code=500, content=error_response(code=ErrorCode.INTERNAL_ERROR.value, message_key="errors.common.internal", details={}))
