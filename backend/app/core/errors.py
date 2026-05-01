from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.common.exceptions import AppException, ErrorCode
from app.common.responses import error_response
from app.core.logging import get_logger

logger = get_logger(__name__)


def _request_context(request: Request) -> dict[str, object]:
    return {
        "request_id": getattr(request.state, "request_id", None),
        "method": request.method,
        "path": request.url.path,
    }


async def app_exception_handler(request: Request, exc: AppException) -> ORJSONResponse:
    context = _request_context(request)
    context.update({"status_code": exc.status_code, "error_code": exc.code.value, "message_key": exc.message_key})
    if exc.status_code >= 500:
        logger.error("application exception", extra={"event": context})
    else:
        logger.warning("application exception", extra={"event": context})
    return ORJSONResponse(status_code=exc.status_code, content=error_response(code=exc.code.value, message_key=exc.message_key, details=exc.context))


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    context = _request_context(request)
    context.update({"status_code": 422, "error_code": ErrorCode.VALIDATION_ERROR.value, "message_key": "errors.validation.invalid_request", "field_count": len(exc.errors())})
    logger.warning("request validation failed", extra={"event": context})
    return ORJSONResponse(status_code=422, content=error_response(code=ErrorCode.VALIDATION_ERROR.value, message_key="errors.validation.invalid_request", details={"fields": exc.errors()}))


async def generic_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    context = _request_context(request)
    context.update({"status_code": 500, "error_code": ErrorCode.INTERNAL_ERROR.value, "message_key": "errors.common.internal"})
    logger.exception("unhandled exception", extra={"event": context})
    return ORJSONResponse(status_code=500, content=error_response(code=ErrorCode.INTERNAL_ERROR.value, message_key="errors.common.internal", details={}))
