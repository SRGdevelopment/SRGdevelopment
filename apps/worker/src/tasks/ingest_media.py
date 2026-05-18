from ..celery_app import celery_app


@celery_app.task
def ingest_media(source: str = "podcast", content: str = ""):
    preview = (content or "Team X has a strong scheduling edge tonight.")[:120]
    return {
        "media_id": "media_queued_001",
        "source": source,
        "status": "queued",
        "content_preview": preview,
    }
