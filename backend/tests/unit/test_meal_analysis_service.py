from datetime import datetime, timezone

from app.schemas.meal import MealAnalysisRequest
from app.services.ai.meal_analysis_service import meal_analysis_service


def test_meal_analysis_shape() -> None:
    req = MealAnalysisRequest(image_id="img1", meal_type="lunch", consumed_at=datetime.now(timezone.utc))
    out = meal_analysis_service.analyze(req)
    assert out.analysis_confidence >= 0
    assert len(out.items) > 0
