from fastapi import APIRouter, Depends

from app.core.deps import get_current_user_id
from app.schemas.user import WeightCreate

router = APIRouter()


@router.post("")
def create_weight(payload: WeightCreate, user_id: str = Depends(get_current_user_id)) -> dict[str, bool]:
    return {"ok": True}


@router.get("")
def get_weights(user_id: str = Depends(get_current_user_id)) -> dict[str, list[dict[str, float]]]:
    return {"items": [{"weight_kg": 79.8}]}
