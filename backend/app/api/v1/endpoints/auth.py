from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.localization import locale_from_header
from app.schemas.auth import LoginRequest, OAuthRequest, RefreshRequest, RegisterRequest, TokenPair
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=TokenPair)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenPair:
    return auth_service.register(db, payload)


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db), locale: str = Depends(locale_from_header)) -> TokenPair:
    return auth_service.login(db, payload, locale)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest) -> TokenPair:
    return auth_service.refresh(payload.refresh_token)


@router.post("/logout")
def logout() -> dict[str, bool]:
    return {"ok": True}


@router.post("/oauth/google", response_model=TokenPair)
def oauth_google(payload: OAuthRequest) -> TokenPair:
    return auth_service.oauth_exchange("google", payload.id_token)


@router.post("/oauth/apple", response_model=TokenPair)
def oauth_apple(payload: OAuthRequest) -> TokenPair:
    return auth_service.oauth_exchange("apple", payload.id_token)
