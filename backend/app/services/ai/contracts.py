from pydantic import BaseModel, Field, field_validator


class VisionItem(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    grams: float = Field(gt=0, le=2500)
    confidence: float = Field(ge=0, le=1)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().lower()


class VisionAnalysis(BaseModel):
    dish_name: str = Field(min_length=1, max_length=128)
    analysis_confidence: float = Field(ge=0, le=1)
    items: list[VisionItem] = Field(min_length=1, max_length=32)


class RecommendationOutput(BaseModel):
    summary: str = Field(min_length=1, max_length=500)
    confidence: float = Field(ge=0, le=1)
