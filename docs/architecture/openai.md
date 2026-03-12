# OpenAI Integration

## Model Strategy
- Vision: `OPENAI_MODEL_VISION` (default gpt-4.1-mini)
- Text generation: `OPENAI_MODEL_TEXT`

## Prompt Versioning
- Prompt templates stored in `backend/app/services/ai/prompts.py`.
- Persist `prompt_version` per analysis/recommendation in future migration.

## Structured Output
- JSON schema in `backend/app/services/ai/schemas.py`.
- Reject malformed output and return safe fallback requiring manual edit.

## Retry/Timeout
- Timeout 25s
- Retry: 2 attempts on transient failures (future Celery policy).

## Safety
- No execution of model or OCR instructions.
- Sanitize and bound all numeric outputs.
