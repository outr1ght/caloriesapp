# Launch Readiness Notes

## Local development checklist
- Start dependencies (`postgres`, `redis`, `minio`) via compose.
- Apply backend migrations.
- Verify backend health endpoint (`/api/v1/health`).
- Run backend tests (`pytest -q`).
- Run Flutter tests (`flutter test`).
- Run app with explicit `API_BASE_URL` and validate login/report flows.

## Troubleshooting
- `401` on protected routes:
  - verify access token is attached
  - verify refresh token endpoint is reachable (`/api/v1/auth/refresh`)
- Upload completion fails:
  - verify object exists in S3 bucket
  - verify `APP_S3_*` credentials and endpoint
- Barcode not found:
  - expected for unsupported providers or unknown codes

## Known MVP risks
- AI reasoning output can degrade during provider outages; fallback warnings are returned.
- Nutritional values are estimates and must be user-reviewed.
- Locale catalogs are partial for backend error messages and may fallback to English.

## Disclaimer references
- App is not a medical device.
- Users must verify dietary decisions.
- AI meal analysis is assistive, not authoritative.
