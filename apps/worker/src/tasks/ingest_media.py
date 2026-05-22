from ..celery_app import celery_app

@celery_app.task
def ingest_media():
    return "TODO: ingest_media"
