# Infrastructure Notes

- `docker-compose.yml` runs local stack: postgres, redis, minio, backend, celery worker, meal vision service.
- For production, split into managed DB/Redis/object storage and deploy backend/workers separately.
