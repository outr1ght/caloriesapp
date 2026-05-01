import httpx
import pytest

from app.integrations.openai_client import OpenAIClient


@pytest.mark.asyncio
async def test_openai_not_configured_returns_warning(monkeypatch):
    client = OpenAIClient()
    monkeypatch.setattr(client.settings, "openai_api_key", None)
    data = await client.generate_json(prompt="test", schema={"type": "object"})
    assert "openai_not_configured" in data["warnings"]


@pytest.mark.asyncio
async def test_openai_retry_exhausted_returns_warning(monkeypatch):
    client = OpenAIClient()
    monkeypatch.setattr(client.settings, "openai_api_key", "test-key")
    monkeypatch.setattr(client.settings, "openai_max_retries", 1)

    async def _request_response_data(*, headers, payload):
        _ = (headers, payload)
        raise httpx.ConnectError("boom")

    async def _sleep_before_retry(attempt: int) -> None:
        _ = attempt
        return None

    monkeypatch.setattr(client, "_request_response_data", _request_response_data)
    monkeypatch.setattr(client, "_sleep_before_retry", _sleep_before_retry)

    data = await client.generate_json(prompt="test", schema={"type": "object"})
    assert data["warnings"] == ["openai_unavailable"]


@pytest.mark.asyncio
async def test_openai_malformed_json_returns_warning(monkeypatch):
    client = OpenAIClient()
    monkeypatch.setattr(client.settings, "openai_api_key", "test-key")

    async def _request_response_data(*, headers, payload):
        _ = (headers, payload)
        return {"output": [{"content": [{"type": "output_text", "text": "{"}]}]}

    monkeypatch.setattr(client, "_request_response_data", _request_response_data)

    data = await client.generate_json(prompt="test", schema={"type": "object"})
    assert data["warnings"] == ["openai_output_invalid"]


def test_openai_parse_output_empty():
    client = OpenAIClient()
    parsed = client._parse_output({"output": []})
    assert parsed["warnings"] == ["empty_openai_output"]
