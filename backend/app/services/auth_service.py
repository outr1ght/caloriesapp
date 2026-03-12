from hashlib import sha256

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.localization import t
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    parse_subject_from_token,
    verify_password,
)
from app.db.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair


class AuthService:
    def register(self, db: Session, req: RegisterRequest) -> TokenPair:
        exists = db.scalar(select(User).where(User.email == req.email.lower()))
        if exists:
            raise HTTPException(status_code=409, detail="Email already registered")

        user = User(email=req.email.lower(), password_hash=hash_password(req.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return TokenPair(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))

    def login(self, db: Session, req: LoginRequest, locale: str) -> TokenPair:
        user = db.scalar(select(User).where(User.email == req.email.lower(), User.deleted_at.is_(None)))
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail=t("auth.invalid", locale))
        return TokenPair(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id))

    def refresh(self, refresh_token: str) -> TokenPair:
        subject = parse_subject_from_token(refresh_token, expected_type="refresh")
        if not subject:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return TokenPair(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))

    def oauth_exchange(self, provider: str, id_token: str) -> TokenPair:
        # MVP placeholder: external provider validation is implemented in a dedicated auth adapter later.
        if not id_token:
            raise HTTPException(status_code=400, detail="Missing id_token")
        subject = sha256(f"{provider}:{id_token}".encode("utf-8")).hexdigest()[:32]
        return TokenPair(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))


auth_service = AuthService()
