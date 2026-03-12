from pydantic import BaseModel, ConfigDict

from app.db.models.domain_enums import RecommendationStatus


class RecommendationUpdateStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: RecommendationStatus
