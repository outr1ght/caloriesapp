from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import ModelBase
from app.db.models.enums import AuthProvider, LanguageCode, UserRole
from app.db.models.mixins import SoftDeleteMixin


class User(ModelBase, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users__email"), Index("ix_users__email_is_active", "email", "is_active"))

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role", native_enum=False), nullable=False, default=UserRole.USER, server_default=UserRole.USER.value)
    locale: Mapped[LanguageCode] = mapped_column(Enum(LanguageCode, name="language_code", native_enum=False), nullable=False, default=LanguageCode.EN, server_default=LanguageCode.EN.value)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC", server_default="UTC")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    auth_identities: Mapped[list["AuthIdentity"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    profile: Mapped["UserProfile | None"] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True, uselist=False)


class AuthIdentity(ModelBase):
    __tablename__ = "auth_identities"
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_auth_identities__provider_provider_user_id"),
        Index("ix_auth_identities__user_provider", "user_id", "provider"),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider, name="auth_provider", native_enum=False), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_email: Mapped[str | None] = mapped_column(String(320), nullable=True)

    user: Mapped["User"] = relationship(back_populates="auth_identities")


class UserProfile(ModelBase, SoftDeleteMixin):
    __tablename__ = "user_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_profiles__user_id"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_year: Mapped[int | None] = mapped_column(nullable=True)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="profile")
