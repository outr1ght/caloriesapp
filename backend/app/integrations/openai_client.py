import asyncio
import json
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
_RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


class OpenAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://api.openai.com/v1"

    async def generate_json(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        model = self.settings.openai_model
        if not self.settings.openai_api_key:
            logger.warning("openai not configured", extra={"event": {"event": "openai_not_configured", "model": model}})
            logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "openai_not_configured"}})
            return {"text": "", "items": [], "warnings": ["openai_not_configured"]}

        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "input": prompt,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "nutrition_reasoning", "schema": schema},
            },
        }

        retries = max(self.settings.openai_max_retries, 0)
        max_attempts = retries + 1
        for attempt in range(1, max_attempts + 1):
            try:
                data = await self._request_response_data(headers=headers, payload=payload)
                self._log_usage(data, model=model)
                parsed = self._parse_output(data)
                if parsed.get("warnings") == ["empty_openai_output"]:
                    logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "empty_openai_output"}})
                return parsed
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                retryable = status_code in _RETRYABLE_STATUS_CODES
                logger.warning(
                    "openai request failed",
                    extra={
                        "event": {
                            "event": "openai_request_failed",
                            "model": model,
                            "attempt": attempt,
                            "max_attempts": max_attempts,
                            "retryable": retryable,
                            "status_code": status_code,
                            "error_type": type(exc).__name__,
                        }
                    },
                )
                if retryable and attempt < max_attempts:
                    await self._sleep_before_retry(attempt)
                    continue
                if retryable:
                    logger.warning("openai retries exhausted", extra={"event": {"event": "openai_retry_exhausted", "model": model, "attempts": attempt}})
                logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "openai_unavailable"}})
                return {"text": "", "items": [], "warnings": ["openai_unavailable"]}
            except (httpx.TimeoutException, httpx.RequestError) as exc:
                logger.warning(
                    "openai request failed",
                    extra={
                        "event": {
                            "event": "openai_request_failed",
                            "model": model,
                            "attempt": attempt,
                            "max_attempts": max_attempts,
                            "retryable": True,
                            "status_code": None,
                            "error_type": type(exc).__name__,
                        }
                    },
                )
                if attempt < max_attempts:
                    await self._sleep_before_retry(attempt)
                    continue
                logger.warning("openai retries exhausted", extra={"event": {"event": "openai_retry_exhausted", "model": model, "attempts": attempt}})
                logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "openai_unavailable"}})
                return {"text": "", "items": [], "warnings": ["openai_unavailable"]}
            except (json.JSONDecodeError, ValueError) as exc:
                logger.warning(
                    "openai output invalid",
                    extra={
                        "event": {
                            "event": "openai_output_invalid",
                            "model": model,
                            "error_type": type(exc).__name__,
                        }
                    },
                )
                logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "openai_output_invalid"}})
                return {"text": "", "items": [], "warnings": ["openai_output_invalid"]}

        logger.warning("openai retries exhausted", extra={"event": {"event": "openai_retry_exhausted", "model": model, "attempts": max_attempts}})
        logger.info("openai fallback used", extra={"event": {"event": "openai_fallback_used", "model": model, "reason": "openai_unavailable"}})
        return {"text": "", "items": [], "warnings": ["openai_unavailable"]}

    async def _request_response_data(self, *, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.settings.openai_timeout_seconds) as client:
            response = await client.post(f"{self.base_url}/responses", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def _sleep_before_retry(self, attempt: int) -> None:
        delay_seconds = min(0.25 * (2 ** (attempt - 1)), 1.0)
        await asyncio.sleep(delay_seconds)

    def _log_usage(self, data: dict[str, Any], *, model: str) -> None:
        usage = data.get("usage")
        if not isinstance(usage, dict):
            return

        prompt_tokens = usage.get("input_tokens", usage.get("prompt_tokens"))
        completion_tokens = usage.get("output_tokens", usage.get("completion_tokens"))
        total_tokens = usage.get("total_tokens")

        if prompt_tokens is None and completion_tokens is None and total_tokens is None:
            return

        logger.info(
            "openai usage",
            extra={
                "event": {
                    "event": "openai_usage",
                    "model": model,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                }
            },
        )

    def _parse_output(self, data: dict[str, Any]) -> dict[str, Any]:
        output_text = ""
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text += str(content.get("text", ""))

        if not output_text:
            return {"text": "", "items": [], "warnings": ["empty_openai_output"]}

        parsed = json.loads(output_text)
        if not isinstance(parsed, dict):
            raise ValueError("OpenAI response is not a JSON object")
        return parsed
