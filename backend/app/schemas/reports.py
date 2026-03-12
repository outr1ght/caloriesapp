from datetime import date
from pydantic import BaseModel


class ReportSummary(BaseModel):
    period: str
    start_date: date
    end_date: date
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float
