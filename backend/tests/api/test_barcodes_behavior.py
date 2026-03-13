import pytest

from app.common.exceptions import AppException, ErrorCode
from app.schemas.barcode import BarcodeLookupResponse
from app.services.barcode_service import BarcodeService


@pytest.mark.usefixtures("auth_overrides")
def test_barcode_lookup_provider_failure_maps_to_not_found(client, monkeypatch):
    async def _lookup(self, code):
        _ = (self, code)
        return BarcodeLookupResponse(found=False, product=None)

    monkeypatch.setattr(BarcodeService, "lookup", _lookup)

    response = client.post("/api/v1/barcodes/lookup", json={"code": "1234567890123"})
    assert response.status_code == 200
    assert response.json()["data"]["found"] is False


@pytest.mark.usefixtures("auth_overrides")
def test_barcode_lookup_validation(client):
    response = client.post("/api/v1/barcodes/lookup", json={"code": "@@@"})
    assert response.status_code == 422


@pytest.mark.usefixtures("auth_overrides")
def test_barcode_lookup_service_error(client, monkeypatch):
    async def _lookup(self, code):
        _ = (self, code)
        raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.barcodes.provider_unavailable", status_code=503)

    monkeypatch.setattr(BarcodeService, "lookup", _lookup)

    response = client.post("/api/v1/barcodes/lookup", json={"code": "1234567890123"})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == ErrorCode.INTERNAL_ERROR.value
