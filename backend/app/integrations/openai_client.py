import json
from typing import Any

import httpx

from app.core.config import get_settings


class OpenAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://api.openai.com/v1"

    async def generate_json(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.openai_api_key:
            return {"text": "", "items": [], "warnings": ["openai_not_configured"]}

        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.openai_model,
            "input": prompt,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "nutrition_reasoning", "schema": schema},
            },
        }

        retries = max(self.settings.openai_max_retries, 0)
        attempt = 0
        while True:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=self.settings.openai_timeout_seconds) as client:
                    response = await client.post(f"{self.base_url}/responses", headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                return self._parse_output(data)
            except (httpx.TimeoutException, httpx.HTTPError, json.JSONDecodeError, ValueError):
                if attempt > retries:
                    return {"text": "", "items": [], "warnings": ["openai_unavailable"]}

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
