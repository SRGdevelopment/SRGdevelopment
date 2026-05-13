from ..celery_app import celery_app

@celery_app.task
def extract_claims():
    return "TODO: extract_claims"
