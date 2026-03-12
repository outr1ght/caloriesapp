from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id, get_db
from app.services.reports.report_service import report_service

router = APIRouter()


@router.get("/daily")
def daily(
    day: date = Query(default_factory=date.today),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    return report_service.build(db=db, user_id=user_id, period="daily", day=day)


@router.get("/weekly")
def weekly(
    day: date = Query(default_factory=date.today),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    start = day - timedelta(days=day.weekday())
    return report_service.build(db=db, user_id=user_id, period="weekly", day=start)


@router.get("/monthly")
def monthly(
    year: int = Query(ge=2000, le=2100),
    month: int = Query(ge=1, le=12),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    target = date(year, month, 1)
    return report_service.build(db=db, user_id=user_id, period="monthly", day=target)
