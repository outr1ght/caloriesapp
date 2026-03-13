# Deployment Notes

## Environments
- `dev`: docker-compose local stack.
- `staging`: k8s namespace with managed DB/Redis/S3.
- `prod`: k8s production namespace with autoscaling.

## Backend Runtime Requirements
- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_REDIS_URL`
- `APP_S3_ENDPOINT_URL`, `APP_S3_ACCESS_KEY_ID`, `APP_S3_SECRET_ACCESS_KEY`, `APP_S3_BUCKET`
- `APP_OPENAI_API_KEY`
- `APP_OPENAI_MODEL`
- `APP_CORS_ORIGINS`

## Health and Observability
- API health: `/api/v1/health`
- Structured logs in stdout for centralized aggregation
- Optional monitoring hooks can be wired via platform env (for example Sentry DSN)

## Migration Strategy
- Always run migrations before API rollout.
- Migration command: `alembic upgrade head`

## Scaling
- API: horizontal pod autoscaling on CPU and request latency.
- Worker: scale by queue depth and task runtime.

## Security
- Secrets injected from secret manager.
- HTTPS termination at ingress/load balancer.
- Restrict CORS to known origins in non-dev environments.
- Rotate API and storage credentials regularly.
