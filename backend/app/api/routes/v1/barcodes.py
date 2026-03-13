from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.user import User
from app.schemas.barcode import BarcodeLookupRequest
from app.services.barcode_service import BarcodeService

router = APIRouter(prefix="/barcodes", tags=["barcodes"])


@router.post("/lookup")
async def lookup_barcode(
    payload: BarcodeLookupRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    result = await BarcodeService(session).lookup(payload.code)
    return success_response(data=result.model_dump())
