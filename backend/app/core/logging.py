import json
import logging
import logging.config
from typing import Any

SENSITIVE_KEYS = {"password", "hashed_password", "token", "access_token", "refresh_token", "authorization", "secret", "api_key"}


class RedactingJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "time": self.formatTime(record, self.datefmt),
        }
        return json.dumps(self._redact_mapping(payload), ensure_ascii=True)

    def _redact_mapping(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: ("***REDACTED***" if k.lower() in SENSITIVE_KEYS else self._redact_mapping(v)) for k, v in value.items()}
        if isinstance(value, list):
            return [self._redact_mapping(item) for item in value]
        return value


def configure_logging() -> None:
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"json": {"()": "app.core.logging.RedactingJsonFormatter"}},
        "handlers": {"default": {"class": "logging.StreamHandler", "formatter": "json", "level": "INFO"}},
        "root": {"handlers": ["default"], "level": "INFO"},
    })
