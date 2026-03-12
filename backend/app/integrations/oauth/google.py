import httpx

from app.common.exceptions import AppException, ErrorCode
from app.integrations.oauth.base import OAuthProvider, OAuthUserInfo


class GoogleOAuthProvider(OAuthProvider):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        _ = code
        _ = redirect_uri
        if not id_token:
            raise AppException(code=ErrorCode.VALIDATION_ERROR, message_key="errors.auth.oauth_missing_token", status_code=422)
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token})
            if response.status_code != 200:
                raise AppException(code=ErrorCode.AUTH_UNAUTHORIZED, message_key="errors.auth.oauth_invalid_token", status_code=401)
            data = response.json()
        return OAuthUserInfo(provider_user_id=str(data.get("sub", "")), email=data.get("email"), email_verified=str(data.get("email_verified", "false")).lower() == "true", display_name=data.get("name"))
