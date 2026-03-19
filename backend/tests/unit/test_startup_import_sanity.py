from datetime import datetime, UTC

from app.main import app
from app.schemas.auth import AuthUserDTO, LogoutRequest, RefreshTokenRequest, RegisterRequest, TokenPairDTO
from app.schemas.barcode import BarcodeLookupResponse
from app.schemas.profile import MeDTO
from app.db.models.enums import LanguageCode, UserRole


def test_startup_entry_imports() -> None:
    assert app.title


def test_auth_schema_field_declarations() -> None:
    register = RegisterRequest(email="user@example.com", password="x" * 8)
    assert register.email == "user@example.com"

    payload = RefreshTokenRequest(refresh_token="x" * 32)
    assert payload.refresh_token == "x" * 32
    assert LogoutRequest(refresh_token=None).refresh_token is None

    token_pair = TokenPairDTO(access_token="token", refresh_token="y" * 32, expires_in=900)
    assert token_pair.refresh_token == "y" * 32

    user = AuthUserDTO(
        id="u1",
        email="user@example.com",
        role=UserRole.USER,
        locale=LanguageCode.EN,
        timezone="UTC",
        is_active=True,
        is_verified=False,
        created_at=datetime.now(UTC),
    )
    assert user.email == "user@example.com"


def test_profile_schema_email_typing_shape() -> None:
    me = MeDTO(
        id="u1",
        email="user@example.com",
        role=UserRole.USER,
        locale=LanguageCode.EN,
        timezone="UTC",
        is_active=True,
        is_verified=False,
        created_at=datetime.now(UTC),
        profile=None,
    )
    assert me.email == "user@example.com"


def test_barcode_response_typing_shape() -> None:
    payload = BarcodeLookupResponse(found=True, product={"product_id": "p1", "name": "Item"})
    assert payload.product and payload.product["product_id"] == "p1"
