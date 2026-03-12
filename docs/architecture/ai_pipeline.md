# AI Pipeline

## Hybrid Pipeline
1. Vision inference (OpenAI Vision in MVP; pluggable adapters later)
2. Ingredient extraction and normalization
3. Deterministic nutrient aggregation from nutrition DB
4. OpenAI text generation for recommendations and plans

## Confidence and Uncertainty
- Every detected ingredient has `confidence`.
- Meal-level `analysis_confidence` computed as weighted average.
- If confidence < threshold (0.65), `requires_manual_review=true`.

## Safety Controls
- Strict JSON schema validation for model outputs.
- Prompt versioning (`prompt_version` persisted on analysis rows).
- Timeout + retry with capped attempts.
- Prompt-injection mitigation: never execute image-derived instructions.

## Cost Controls
- Small model by default for recommendations.
- Vision calls limited by image size and request quotas.
- Cache recent identical image hash results for short TTL.
