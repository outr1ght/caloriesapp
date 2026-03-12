# API Examples

See OpenAPI at `/docs` when backend runs.

## Analyze Photo
POST `/api/v1/meals/analyze-photo`

Request:
```json
{
  "image_id": "uuid",
  "meal_type": "lunch",
  "consumed_at": "2026-03-10T12:30:00Z"
}
```

Response:
```json
{
  "analysis_id": "uuid",
  "analysis_confidence": 0.72,
  "requires_manual_review": false,
  "items": [
    {"name": "chicken breast", "grams": 160, "confidence": 0.81}
  ],
  "nutrition": {"calories": 410, "protein_g": 38, "fat_g": 14, "carbs_g": 22},
  "disclaimer_key": "nutrition.approximate"
}
```
