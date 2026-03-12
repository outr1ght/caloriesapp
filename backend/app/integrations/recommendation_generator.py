from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.common.exceptions import AppException, ErrorCode
from app.integrations.openai_client import OpenAIClient


class RecommendationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1, max_length=4096)
    warnings: list[str] = Field(default_factory=list)


class RecommendationGenerator:
    def __init__(self) -> None:
        self.client = OpenAIClient()

    async def generate(self, context: str) -> RecommendationOutput:
        schema = {"type": "object", "properties": {"title": {"type": "string"}, "body": {"type": "string"}, "warnings": {"type": "array", "items": {"type": "string"}}}, "required": ["title", "body", "warnings"], "additionalProperties": False}
        raw = await self.client.generate_json(prompt=f"Generate concise nutrition recommendation. Context:\n{context}", schema=schema)
        try:
            return RecommendationOutput.model_validate(raw)
        except ValidationError as exc:
            raise AppException(code=ErrorCode.INTERNAL_ERROR, message_key="errors.recommendations.invalid_ai_output", status_code=500, context={"reason": str(exc)}) from exc
