from typing import Any


def success_response(*, data: Any, message_key: str = "messages.common.success", meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"ok": True, "message_key": message_key, "data": data, "error": None, "meta": meta or {}}


def error_response(*, code: str, message_key: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"ok": False, "message_key": message_key, "data": None, "error": {"code": code, "details": details or {}}, "meta": {}}
