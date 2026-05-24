from ..celery_app import celery_app


@celery_app.task
def ingest_sports_context(league: str = "NBA"):
    return {
        "league": league,
        "items": [
            {"type": "injury", "team": "BOS", "impact": 0.12},
            {"type": "rest", "team": "NYK", "impact": -0.04},
        ],
    }
