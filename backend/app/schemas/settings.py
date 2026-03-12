from typing import Any

from pydantic import BaseModel, ConfigDict

from app.db.models.domain_enums import UnitSystem
from app.db.models.enums import LanguageCode


class UserSettingsUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: LanguageCode | None = None
    unit_system: UnitSystem | None = None
    notifications_enabled: bool | None = None
    meal_reminder_enabled: bool | None = None
    privacy_flags: dict[str, Any] | None = None
    feature_flags: dict[str, Any] | None = None


class UserSettingsDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    user_id: str
    language: LanguageCode
    unit_system: UnitSystem
    notifications_enabled: bool
    meal_reminder_enabled: bool
    privacy_flags: dict[str, Any] | None
    feature_flags: dict[str, Any] | None
