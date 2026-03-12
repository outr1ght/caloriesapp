from app.schemas.barcode import BarcodeLookupRequest

def test_barcode_lookup_payload() -> None:
    assert BarcodeLookupRequest(code="1234567890123").code == "1234567890123"
