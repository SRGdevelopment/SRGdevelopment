from ..celery_app import celery_app

@celery_app.task
def run_predictions():
    return "TODO: run_predictions"
