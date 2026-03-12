# Deployment Notes

## Environments
- `dev`: docker-compose local stack.
- `staging`: k8s namespace with managed DB/Redis/S3.
- `prod`: k8s production namespace with autoscaling.

## Backend Runtime Requirements
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`
- `OPENAI_API_KEY`
- `SENTRY_DSN`

## Health and Observability
- API health: `/healthz`
- Sentry SDK enabled by `SENTRY_DSN`
- Structured logs in stdout for centralized aggregation

## Migration Strategy
- Always run migrations before API rollout.
- Migration command: `alembic upgrade head`
- Non-prod seed: `python -m scripts.seed_data`

## Scaling
- API: horizontal pod autoscaling on CPU and request latency.
- Worker: scale by queue depth and task runtime.

## Security
- Secrets injected from secret manager.
- HTTPS termination at ingress/load balancer.
- Restrict CORS to known origins in non-dev environments.
