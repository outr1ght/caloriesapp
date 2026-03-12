from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User, UserProfile, NutritionGoal, UserSetting
from app.db.models.enums import LocaleCode, UnitSystem


class UserRepository:
    def get_active_by_id(self, db: Session, user_id: str) -> User | None:
        return db.scalar(select(User).where(User.id == user_id, User.deleted_at.is_(None)))

    def ensure_profile(self, db: Session, user_id: str) -> UserProfile:
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
        if profile:
            return profile
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        db.flush()
        return profile

    def ensure_goals(self, db: Session, user_id: str) -> NutritionGoal:
        goals = db.scalar(select(NutritionGoal).where(NutritionGoal.user_id == user_id))
        if goals:
            return goals
        goals = NutritionGoal(user_id=user_id, calorie_target=2000)
        db.add(goals)
        db.flush()
        return goals

    def ensure_settings(self, db: Session, user_id: str) -> UserSetting:
        settings = db.scalar(select(UserSetting).where(UserSetting.user_id == user_id))
        if settings:
            return settings
        settings = UserSetting(user_id=user_id, locale=LocaleCode.EN, unit_system=UnitSystem.METRIC)
        db.add(settings)
        db.flush()
        return settings


user_repository = UserRepository()
