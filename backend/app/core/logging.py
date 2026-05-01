import json
import logging
import logging.config
from typing import Any

SENSITIVE_KEYS = {"password", "hashed_password", "token", "access_token", "refresh_token", "authorization", "secret", "api_key"}
_DEFAULT_LOG_RECORD_KEYS = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys())


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

        event = getattr(record, "event", None)
        if isinstance(event, dict):
            payload.update(event)

        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _DEFAULT_LOG_RECORD_KEYS and key not in {"message", "asctime", "event"} and not key.startswith("_")
        }
        if extras:
            payload["extra"] = extras

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

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


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
