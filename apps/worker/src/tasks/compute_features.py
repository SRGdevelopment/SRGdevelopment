from ..celery_app import celery_app

@celery_app.task
def compute_features():
    return "TODO: compute_features"
