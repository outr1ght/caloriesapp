import pytest

from app.schemas.barcode import BarcodeLookupResponse
from app.services.barcode_service import BarcodeService


class _Result:
    def scalar_one_or_none(self):
        return None


class _Session:
    def __init__(self):
        self.add_calls = []

    async def execute(self, stmt):
        _ = stmt
        return _Result()

    def add(self, value):
        self.add_calls.append(value)

    async def flush(self):
        return None

    async def commit(self):
        return None


class _FailingProvider:
    async def lookup(self, code: str):
        _ = code
        raise RuntimeError("provider down")


class _MalformedProvider:
    async def lookup(self, code: str):
        _ = code
        return {"name": "X", "nutrition": {"calories": "not-a-number"}}


@pytest.mark.asyncio
async def test_provider_failure_returns_not_found():
    service = BarcodeService(session=_Session(), provider=_FailingProvider())
    result = await service.lookup("1234567890123")
    assert isinstance(result, BarcodeLookupResponse)
    assert result.found is False


@pytest.mark.asyncio
async def test_malformed_provider_payload_returns_not_found():
    service = BarcodeService(session=_Session(), provider=_MalformedProvider())
    result = await service.lookup("1234567890123")
    assert result.found is False
    assert result.product is None
