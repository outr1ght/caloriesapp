from datetime import date
from sqlalchemy.orm import Session

from app.db.repositories.report_repository import report_repository
from app.schemas.reports import ReportSummary


class ReportService:
    def build(self, db: Session, user_id: str, period: str, day: date) -> ReportSummary:
        totals = report_repository.nutrition_totals(db=db, user_id=user_id, day=day, period=period)

        if period == "daily":
            start_date = day
            end_date = day
        elif period == "weekly":
            start_date = day
            end_date = day
        else:
            start_date = day.replace(day=1)
            end_date = day.replace(day=28)

        return ReportSummary(
            period=period,
            start_date=start_date,
            end_date=end_date,
            calories=totals["calories"],
            protein_g=totals["protein_g"],
            fat_g=totals["fat_g"],
            carbs_g=totals["carbs_g"],
        )


report_service = ReportService()
