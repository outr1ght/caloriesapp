from app.services.barcode.barcode_service import barcode_service


def test_barcode_not_found() -> None:
    out = barcode_service.scan('0000')
    assert out.found is False
