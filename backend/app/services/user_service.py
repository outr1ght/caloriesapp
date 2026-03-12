from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repositories.user_repository import user_repository
from app.schemas.user import GoalsPatch, MeResponse, ProfilePatch, SettingsPatch


class UserService:
    def me(self, db: Session, user_id: str) -> MeResponse:
        user = user_repository.get_active_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        settings = user_repository.ensure_settings(db, user_id)
        db.commit()

        return MeResponse(
            user_id=user.id,
            email=user.email,
            locale=str(settings.locale.value),
            unit_system=str(settings.unit_system.value),
        )

    def patch_profile(self, db: Session, user_id: str, payload: ProfilePatch) -> None:
        user = user_repository.get_active_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = user_repository.ensure_profile(db, user_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        db.commit()

    def patch_settings(self, db: Session, user_id: str, payload: SettingsPatch) -> None:
        user = user_repository.get_active_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        settings = user_repository.ensure_settings(db, user_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(settings, field, value)
        db.commit()

    def patch_goals(self, db: Session, user_id: str, payload: GoalsPatch) -> None:
        user = user_repository.get_active_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        goals = user_repository.ensure_goals(db, user_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(goals, field, value)
        db.commit()


user_service = UserService()
