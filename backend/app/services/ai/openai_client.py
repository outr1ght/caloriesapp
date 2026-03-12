from __future__ import annotations

import asyncio
from typing import Any

import httpx

from app.core.config import settings


class OpenAIClient:
    def __init__(self) -> None:
        self.timeout = 25.0
        self.max_retries = 2

    async def responses_json(self, prompt: str, schema: dict, model: str | None = None) -> dict[str, Any]:
        if not settings.openai_api_key:
            return {"fallback": True, "reason": "missing_api_key"}

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or settings.openai_model_text,
            "input": prompt,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "nutrition_response", "schema": schema, "strict": True},
            },
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post("https://api.openai.com/v1/responses", headers=headers, json=payload)
                    response.raise_for_status()
                    body = response.json()
                    output = self._extract_output_json(body)
                    if output is None:
                        return {"fallback": True, "reason": "malformed_output"}
                    return output
            except (httpx.TimeoutException, httpx.HTTPError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.6 * (attempt + 1))

        return {"fallback": True, "reason": f"request_failed:{type(last_error).__name__}"}

    @staticmethod
    def _extract_output_json(body: dict[str, Any]) -> dict[str, Any] | None:
        output = body.get("output")
        if not isinstance(output, list):
            return None

        for item in output:
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if part.get("type") == "output_json" and isinstance(part.get("json"), dict):
                    return part["json"]
                if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    # For safety, do not parse non-JSON model text in MVP.
                    return None
        return None


openai_client = OpenAIClient()
