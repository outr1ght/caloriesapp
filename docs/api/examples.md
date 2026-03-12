# API Payload Examples

## POST /api/v1/auth/register
Request:
```json
{"email":"user@example.com","password":"StrongPass123"}
```
Response:
```json
{"access_token":"...","refresh_token":"...","token_type":"bearer"}
```

## POST /api/v1/uploads/image
Multipart form `file=image/jpeg`
Response:
```json
{"image_id":"img_demo","upload_url":"s3://placeholder/img_demo"}
```

## POST /api/v1/meals/analyze-photo
Request:
```json
{"image_id":"img_demo","meal_type":"lunch","consumed_at":"2026-03-10T12:30:00Z"}
```
Response:
```json
{
  "analysis_id":"uuid",
  "analysis_confidence":0.74,
  "requires_manual_review":false,
  "items":[{"name":"chicken breast","grams":160,"confidence":0.81}],
  "nutrition":{"calories":520,"protein_g":44,"fat_g":13,"carbs_g":56},
  "disclaimer_key":"nutrition.approximate"
}
```

## POST /api/v1/barcodes/scan
Request:
```json
{"code":"737628064502"}
```
Response:
```json
{"found":true,"product_name":"Organic Peanut Butter","brand":"Sample Foods","nutrition_per_100g":{"calories":588,"protein_g":25,"fat_g":50,"carbs_g":20}}
```
