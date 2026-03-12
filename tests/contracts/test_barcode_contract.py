from app.services.barcode.barcode_service import barcode_service


def test_contract_barcode_found() -> None:
    out = barcode_service.scan('737628064502')
    assert out.found is True
    assert out.product_name is not None
