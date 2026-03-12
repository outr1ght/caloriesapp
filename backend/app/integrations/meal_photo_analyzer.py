from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.common.exceptions import AppException, ErrorCode
from app.integrations.openai_client import OpenAIClient


class PhotoItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=255)
    quantity_g: float = Field(gt=0)
    confidence: float = Field(ge=0, le=1)


class MealPhotoAnalysisOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[PhotoItem]
    notes: str = Field(default="", max_length=4096)
    warnings: list[str] = Field(default_factory=list)


class MealPhotoAnalyzer:
    def __init__(self) -> None:
        self.client = OpenAIClient()

    async def analyze(self, image_context: str) -> MealPhotoAnalysisOutput:
        schema = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "quantity_g": {"type": "number"}, "confidence": {"type": "number"}}, "required": ["name", "quantity_g", "confidence"], "additionalProperties": False}}, "notes": {"type": "string"}, "warnings": {"type": "array", "items": {"type": "string"}}}, "required": ["items", "notes", "warnings"], "additionalProperties": False}
        raw = await self.client.generate_json(prompt=f"Estimate visible food items and portions. Context:\n{image_context}", schema=schema)
        try:
            return MealPhotoAnalysisOutput.model_validate(raw)
        except ValidationError as exc:
            raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.analysis.invalid_ai_output", status_code=500, context={"reason": str(exc)}) from exc
