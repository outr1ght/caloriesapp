from fastapi import APIRouter, Depends

from app.core.deps import get_current_user_id
from app.core.localization import locale_from_header
from app.schemas.features import RecommendationResponse
from app.services.recommendations_service import recommendation_service

router = APIRouter()


@router.get("/latest", response_model=RecommendationResponse)
def latest(user_id: str = Depends(get_current_user_id), locale: str = Depends(locale_from_header)) -> RecommendationResponse:
    return recommendation_service.latest(locale)


@router.post("/generate", response_model=RecommendationResponse)
def generate(user_id: str = Depends(get_current_user_id), locale: str = Depends(locale_from_header)) -> RecommendationResponse:
    return recommendation_service.latest(locale)
