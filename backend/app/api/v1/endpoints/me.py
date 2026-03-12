from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id, get_db
from app.schemas.user import GoalsPatch, MeResponse, ProfilePatch, SettingsPatch
from app.services.user_service import user_service

router = APIRouter(prefix="/me")


@router.get("", response_model=MeResponse)
def me(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> MeResponse:
    return user_service.me(db, user_id)


@router.patch("/profile")
def patch_profile(payload: ProfilePatch, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    user_service.patch_profile(db, user_id, payload)
    return {"ok": True}


@router.patch("/settings")
def patch_settings(payload: SettingsPatch, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    user_service.patch_settings(db, user_id, payload)
    return {"ok": True}


@router.patch("/goals")
def patch_goals(payload: GoalsPatch, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    user_service.patch_goals(db, user_id, payload)
    return {"ok": True}
