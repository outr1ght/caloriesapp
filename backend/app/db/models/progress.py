from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import ModelBase
from app.db.models.domain_enums import ActivityLevel, AuditAction, GoalStrategy, RecommendationStatus, RecommendationType, UnitSystem
from app.db.models.enums import LanguageCode
from app.db.models.mixins import SoftDeleteMixin


class NutritionGoal(ModelBase, SoftDeleteMixin):
    __tablename__ = "nutrition_goals"
    __table_args__ = (Index("ix_nutrition_goals__user_id_is_active", "user_id", "is_active"), CheckConstraint("target_calories >= 0", name="nutrition_goals_target_calories_non_negative"))

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    strategy: Mapped[GoalStrategy] = mapped_column(Enum(GoalStrategy, name="goal_strategy", native_enum=False), nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(Enum(ActivityLevel, name="activity_level", native_enum=False), nullable=False)
    target_calories: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    target_protein_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    target_carbs_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    target_fat_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    target_water_ml: Mapped[int | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True, server_default="true")
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Recommendation(ModelBase, SoftDeleteMixin):
    __tablename__ = "recommendations"
    __table_args__ = (Index("ix_recommendations__user_id_created_at", "user_id", "created_at"), Index("ix_recommendations__status", "status"))

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_id: Mapped[str | None] = mapped_column(ForeignKey("meals.id", ondelete="SET NULL"), nullable=True, index=True)
    recommendation_type: Mapped[RecommendationType] = mapped_column(Enum(RecommendationType, name="recommendation_type", native_enum=False), nullable=False)
    status: Mapped[RecommendationStatus] = mapped_column(Enum(RecommendationStatus, name="recommendation_status", native_enum=False), nullable=False, default=RecommendationStatus.PENDING, server_default=RecommendationStatus.PENDING.value)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(String(4096), nullable=False)
    generator: Mapped[str] = mapped_column(String(64), nullable=False, default="hybrid", server_default="hybrid")
    rationale_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    context_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    meal = relationship("Meal", lazy="joined")


class WeightLog(ModelBase, SoftDeleteMixin):
    __tablename__ = "weight_logs"
    __table_args__ = (UniqueConstraint("user_id", "logged_at", name="uq_weight_logs__user_id_logged_at"), CheckConstraint("weight_kg > 0", name="weight_logs_weight_positive"), Index("ix_weight_logs__user_id_logged_at", "user_id", "logged_at"))

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    body_fat_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    note: Mapped[str | None] = mapped_column(String(512), nullable=True)


class UserSettings(ModelBase):
    __tablename__ = "user_settings"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_settings__user_id"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language: Mapped[LanguageCode] = mapped_column(Enum(LanguageCode, name="language_code_settings", native_enum=False), nullable=False, default=LanguageCode.EN, server_default=LanguageCode.EN.value)
    unit_system: Mapped[UnitSystem] = mapped_column(Enum(UnitSystem, name="unit_system", native_enum=False), nullable=False, default=UnitSystem.METRIC, server_default=UnitSystem.METRIC.value)
    notifications_enabled: Mapped[bool] = mapped_column(nullable=False, default=True, server_default="true")
    meal_reminder_enabled: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    privacy_flags: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    feature_flags: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)


class AuditLog(ModelBase):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs__entity_type_entity_id", "entity_type", "entity_id"), Index("ix_audit_logs__actor_user_id_created_at", "actor_user_id", "created_at"))

    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction, name="audit_action", native_enum=False), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ip_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
