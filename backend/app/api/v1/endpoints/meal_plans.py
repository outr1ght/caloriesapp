from uuid import uuid4
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user_id
from app.core.localization import locale_from_header
from app.schemas.features import MealPlanResponse

router = APIRouter()


@router.post("/generate", response_model=MealPlanResponse)
def generate(user_id: str = Depends(get_current_user_id), locale: str = Depends(locale_from_header)) -> MealPlanResponse:
    return MealPlanResponse(id=str(uuid4()), locale=locale, plan_json='{"days": []}')


@router.get("", response_model=list[MealPlanResponse])
def list_plans(user_id: str = Depends(get_current_user_id), locale: str = Depends(locale_from_header)) -> list[MealPlanResponse]:
    return [MealPlanResponse(id=str(uuid4()), locale=locale, plan_json='{"days": []}')]
