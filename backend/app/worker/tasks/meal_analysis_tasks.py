from app.worker.celery_app import celery_app

@celery_app.task(name="meal_analysis.follow_up")
def meal_analysis_follow_up(meal_id: str, user_id: str) -> dict:
    return {"meal_id": meal_id, "user_id": user_id, "status": "scheduled_follow_up"}
