from app.integrations.meal_photo_analyzer import MealPhotoAnalysisOutput
from app.integrations.recommendation_generator import RecommendationOutput

def test_recommendation_output_schema() -> None:
    assert RecommendationOutput(title="Add protein", body="Include eggs", warnings=[]).title

def test_photo_analysis_output_schema() -> None:
    assert MealPhotoAnalysisOutput(items=[], notes="", warnings=["low_confidence"]).warnings == ["low_confidence"]
