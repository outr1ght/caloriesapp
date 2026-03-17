from app.main import app
from app.schemas.auth import LogoutRequest, RefreshTokenRequest, TokenPairDTO
from app.schemas.barcode import BarcodeLookupResponse


def test_startup_entry_imports() -> None:
    assert app.title


def test_auth_schema_field_declarations() -> None:
    payload = RefreshTokenRequest(refresh_token='x' * 32)
    assert payload.refresh_token == 'x' * 32
    assert LogoutRequest(refresh_token=None).refresh_token is None
    token_pair = TokenPairDTO(access_token='token', refresh_token='y' * 32, expires_in=900)
    assert token_pair.refresh_token == 'y' * 32


def test_barcode_response_typing_shape() -> None:
    payload = BarcodeLookupResponse(found=True, product={'product_id': 'p1', 'name': 'Item'})
    assert payload.product and payload.product['product_id'] == 'p1'
