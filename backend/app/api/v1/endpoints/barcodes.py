from fastapi import APIRouter, Depends

from app.core.deps import get_current_user_id
from app.schemas.features import BarcodeScanRequest, BarcodeScanResponse
from app.services.barcode.barcode_service import barcode_service

router = APIRouter()


@router.post("/scan", response_model=BarcodeScanResponse)
def scan(payload: BarcodeScanRequest, user_id: str = Depends(get_current_user_id)) -> BarcodeScanResponse:
    return barcode_service.scan(payload.code)
