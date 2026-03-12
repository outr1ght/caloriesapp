from app.worker.celery_app import celery_app

@celery_app.task(name="recommendations.generate_daily")
def generate_daily_recommendation(user_id: str) -> dict:
    return {"user_id": user_id, "status": "queued_result", "title": "Daily recommendation generated"}
