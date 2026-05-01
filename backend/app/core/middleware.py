from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging import get_logger

logger = get_logger(__name__)
_NOISY_PATHS = {"/api/v1/health", "/docs", "/openapi.json", "/redoc"}


class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {key.decode("latin-1").lower(): value.decode("latin-1") for key, value in scope.get("headers", [])}
        request_id = headers.get("x-request-id") or str(uuid4())
        path = scope.get("path", "")
        method = scope.get("method", "")
        start = perf_counter()
        status_code = 500

        state = scope.setdefault("state", {})
        if isinstance(state, dict):
            state["request_id"] = request_id

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                headers_list = list(message.get("headers", []))
                headers_list.append((b"x-request-id", request_id.encode("latin-1")))
                message["headers"] = headers_list
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            if path not in _NOISY_PATHS:
                duration_ms = round((perf_counter() - start) * 1000, 2)
                logger.info(
                    "request completed",
                    extra={"event": {
                        "request_id": request_id,
                        "method": method,
                        "path": path,
                        "status_code": status_code,
                        "duration_ms": duration_ms,
                    }},
                )

