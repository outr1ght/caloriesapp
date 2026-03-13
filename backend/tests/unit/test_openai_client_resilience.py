import pytest

from app.integrations.openai_client import OpenAIClient


@pytest.mark.asyncio
async def test_openai_not_configured_returns_warning(monkeypatch):
    client = OpenAIClient()
    monkeypatch.setattr(client.settings, "openai_api_key", None)
    data = await client.generate_json(prompt="test", schema={"type": "object"})
    assert "openai_not_configured" in data["warnings"]


def test_openai_parse_output_empty():
    client = OpenAIClient()
    parsed = client._parse_output({"output": []})
    assert parsed["warnings"] == ["empty_openai_output"]
