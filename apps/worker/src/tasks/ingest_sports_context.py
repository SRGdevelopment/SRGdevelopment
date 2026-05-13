from ..celery_app import celery_app

@celery_app.task
def ingest_sports_context():
    return "TODO: ingest_sports_context"
