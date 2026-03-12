from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id, get_db
from app.schemas.meal import MealAnalysisRequest, MealAnalysisResponse, MealCreateRequest, MealListResponse, MealPatchRequest, MealResponse
from app.services.ai.meal_analysis_service import meal_analysis_service
from app.services.meal_service import meal_service

router = APIRouter()


@router.post("/analyze-photo", response_model=MealAnalysisResponse)
def analyze_photo(payload: MealAnalysisRequest, user_id: str = Depends(get_current_user_id)) -> MealAnalysisResponse:
    return meal_analysis_service.analyze(payload)


@router.post("", response_model=MealResponse)
def create_meal(
    payload: MealCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MealResponse:
    return meal_service.create_meal(db=db, user_id=user_id, payload=payload)


@router.get("", response_model=MealListResponse)
def get_meals(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MealListResponse:
    return meal_service.list_meals(db=db, user_id=user_id, page=page, page_size=page_size)


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(meal_id: str, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> MealResponse:
    return meal_service.get_meal(db=db, user_id=user_id, meal_id=meal_id)


@router.patch("/{meal_id}", response_model=MealResponse)
def patch_meal(
    meal_id: str,
    payload: MealPatchRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> MealResponse:
    return meal_service.patch_meal(db=db, user_id=user_id, meal_id=meal_id, payload=payload)


@router.delete("/{meal_id}")
def delete_meal(meal_id: str, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> dict[str, bool]:
    meal_service.delete_meal(db=db, user_id=user_id, meal_id=meal_id)
    return {"ok": True}
