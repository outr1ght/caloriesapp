from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import success_response
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import enforce_user_rate_limit
from app.db.models.user import User
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/nutrition")
async def nutrition_report(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    date_from: date = Query(...),
    date_to: date = Query(...),
) -> dict:
    await enforce_user_rate_limit(request, f"user:{current_user.id}")
    report = await ReportService(session).nutrition_report(current_user.id, date_from, date_to)
    return success_response(data=report.model_dump())
