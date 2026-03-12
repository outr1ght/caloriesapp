from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class OAuthUserInfo:
    provider_user_id: str
    email: str | None
    email_verified: bool
    display_name: str | None = None


class OAuthProvider(Protocol):
    async def resolve_user(self, *, code: str | None, id_token: str | None, redirect_uri: str | None) -> OAuthUserInfo:
        ...
