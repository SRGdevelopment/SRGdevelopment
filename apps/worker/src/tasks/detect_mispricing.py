from ..celery_app import celery_app


@celery_app.task
def detect_mispricing() -> str:
    return "TODO: detect mispricing from latest model+market snapshots"
