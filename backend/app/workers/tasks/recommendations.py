from app.workers.celery_app import celery_app


@celery_app.task(name="recommendations.generate")
def generate_recommendation(user_id: str, locale: str) -> dict[str, str]:
    return {"user_id": user_id, "locale": locale, "status": "generated"}
