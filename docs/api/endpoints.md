# Endpoint Contract Details

## Auth
### POST /api/v1/auth/register
- Auth: public
- Request: `email`, `password(min8)`
- Response: access/refresh tokens
- Errors: 409 email exists, 422 validation

### POST /api/v1/auth/login
- Auth: public
- Request: `email`, `password`
- Response: access/refresh tokens
- Errors: 401 invalid credentials

### POST /api/v1/auth/refresh
- Auth: public with refresh token
- Response: rotated token pair

### POST /api/v1/auth/logout
- Auth: bearer
- Response: `{ ok: true }`

### POST /api/v1/auth/oauth/google|apple
- Auth: public
- Request: `id_token`
- Response: token pair

## Users/Profile
### GET /api/v1/me
- Auth: bearer
- Response: user identity summary

### PATCH /api/v1/me/profile
- Auth: bearer
- Validation: field ranges

### PATCH /api/v1/me/settings
- Auth: bearer
- Validation: locale enum, unit enum

### PATCH /api/v1/me/goals
- Auth: bearer
- Validation: target ranges

## Upload/Analysis
### POST /api/v1/uploads/image
- Auth: bearer
- Validation: MIME and size limits
- Response: `image_id`, `upload_url`

### POST /api/v1/meals/analyze-photo
- Auth: bearer
- Response: items/confidence/nutrition/flags

### POST /api/v1/meals
- Auth: bearer
- Request: corrected items
- Response: saved meal with totals

## Reports
- GET `/daily`, `/weekly`, `/monthly`
- Auth: bearer
- Query: date params

## Recommendations
- GET `/latest`
- POST `/generate`

## Weight
- POST `/weights`, GET `/weights`

## Barcode
- POST `/barcodes/scan`

## Meal Planning
- POST `/meal-plans/generate`, GET `/meal-plans`

## Localization
- GET `/localization/supported-languages`
