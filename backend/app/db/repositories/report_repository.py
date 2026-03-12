from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.models import Meal, MealItem


class ReportRepository:
    def _window(self, day: date, period: str) -> tuple[datetime, datetime]:
        if period == "daily":
            start = datetime.combine(day, time.min, tzinfo=timezone.utc)
            end = datetime.combine(day, time.max, tzinfo=timezone.utc)
            return start, end

        if period == "weekly":
            start_day = day - timedelta(days=day.weekday())
            end_day = start_day + timedelta(days=6)
            return (
                datetime.combine(start_day, time.min, tzinfo=timezone.utc),
                datetime.combine(end_day, time.max, tzinfo=timezone.utc),
            )

        start_day = day.replace(day=1)
        # MVP approximation for month end boundary in repository scaffold.
        end_day = day.replace(day=28)
        return (
            datetime.combine(start_day, time.min, tzinfo=timezone.utc),
            datetime.combine(end_day, time.max, tzinfo=timezone.utc),
        )

    def nutrition_totals(self, db: Session, user_id: str, day: date, period: str) -> dict[str, float]:
        start_at, end_at = self._window(day, period)

        stmt: Select = (
            select(
                func.coalesce(func.sum(MealItem.calories), 0.0),
                func.coalesce(func.sum(MealItem.protein_g), 0.0),
                func.coalesce(func.sum(MealItem.fat_g), 0.0),
                func.coalesce(func.sum(MealItem.carbs_g), 0.0),
            )
            .join(Meal, Meal.id == MealItem.meal_id)
            .where(Meal.user_id == user_id)
            .where(Meal.deleted_at.is_(None))
            .where(MealItem.deleted_at.is_(None))
            .where(Meal.consumed_at >= start_at)
            .where(Meal.consumed_at <= end_at)
        )

        calories, protein_g, fat_g, carbs_g = db.execute(stmt).one()
        return {
            "calories": float(calories),
            "protein_g": float(protein_g),
            "fat_g": float(fat_g),
            "carbs_g": float(carbs_g),
        }


report_repository = ReportRepository()
