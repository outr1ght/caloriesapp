from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.common import TimestampMixin, UUIDMixin
from app.db.models.enums import ActivityLevel, BiologicalSex, LocaleCode, UnitSystem


class UserProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, index=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sex: Mapped[BiologicalSex | None] = mapped_column(Enum(BiologicalSex, native_enum=False), nullable=True)
    height_cm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(nullable=True)
    activity_level: Mapped[ActivityLevel | None] = mapped_column(Enum(ActivityLevel, native_enum=False), nullable=True)
    dietary_preference: Mapped[str | None] = mapped_column(String(32), nullable=True)

    user = relationship("User", back_populates="profile")


class NutritionGoal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "nutrition_goals"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, index=True)
    calorie_target: Mapped[int] = mapped_column(Integer, default=2000)
    protein_target_g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fat_target_g: Mapped[int | None] = mapped_column(Integer, nullable=True)
    carbs_target_g: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user = relationship("User", back_populates="goals")


class UserSetting(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, index=True)
    locale: Mapped[LocaleCode] = mapped_column(Enum(LocaleCode, native_enum=False), default=LocaleCode.EN)
    unit_system: Mapped[UnitSystem] = mapped_column(Enum(UnitSystem, native_enum=False), default=UnitSystem.METRIC)

    user = relationship("User", back_populates="settings")
