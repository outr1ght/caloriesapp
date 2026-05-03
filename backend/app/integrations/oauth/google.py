from datetime import UTC, datetime

import httpx

from app.common.exceptions import AppException, ErrorCode
from app.core.config import get_settings
from app.integrations.oauth.base import OAuthProvider, OAuthUserInfo

_GOOGLE_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}


class GoogleOAuthProvider(OAuthProvider):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        _ = code
        _ = redirect_uri
        if not id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)

        settings = get_settings()
        if not settings.google_oauth_client_id:
            raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.common.internal", status_code=500)

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token})
            if response.status_code != 200:
                raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
            data = response.json()

        issuer = str(data.get("iss", ""))
        audience = str(data.get("aud", ""))
        subject = str(data.get("sub", ""))
        exp_raw = data.get("exp")
        try:
            exp = int(exp_raw)
        except (TypeError, ValueError):
            exp = 0

        if issuer not in _GOOGLE_ISSUERS:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        if audience != settings.google_oauth_client_id:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        if exp <= int(datetime.now(UTC).timestamp()):
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
        if not subject:
            raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)

        return OAuthUserInfo(
            provider_user_id=subject,
            email=data.get("email"),
            email_verified=str(data.get("email_verified", "false")).lower() == "true",
            display_name=data.get("name"),
        )
