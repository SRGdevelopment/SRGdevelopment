from ..celery_app import celery_app

@celery_app.task
def evaluate_claims():
    return "TODO: evaluate_claims"
