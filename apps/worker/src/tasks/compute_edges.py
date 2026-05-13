from ..celery_app import celery_app

@celery_app.task
def compute_edges():
    return "TODO: compute_edges"
