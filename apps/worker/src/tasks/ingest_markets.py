from ..celery_app import celery_app

@celery_app.task
def ingest_markets():
    return "TODO: ingest_markets"
