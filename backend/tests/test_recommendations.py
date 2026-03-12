from app.schemas.recommendations import RecommendationUpdateStatusRequest

def test_recommendation_status_payload() -> None:
    assert RecommendationUpdateStatusRequest(status="dismissed").status.value == "dismissed"
