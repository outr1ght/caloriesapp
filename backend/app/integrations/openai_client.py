from typing import Any

import httpx

from app.core.config import get_settings


class OpenAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://api.openai.com/v1"

    async def generate_json(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.openai_api_key:
            return {"text": "OpenAI key is not configured.", "items": [], "warnings": ["openai_not_configured"]}
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}", "Content-Type": "application/json"}
        payload = {"model": self.settings.openai_model, "input": prompt, "response_format": {"type": "json_schema", "json_schema": {"name": "nutrition_reasoning", "schema": schema}}}
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(f"{self.base_url}/responses", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        output_text = ""
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text += content.get("text", "")
        if not output_text:
            return {"text": "", "items": [], "warnings": ["empty_openai_output"]}
        import json
        return json.loads(output_text)
