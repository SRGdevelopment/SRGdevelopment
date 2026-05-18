from ..celery_app import celery_app


@celery_app.task
def compute_edges(model_probability: float = 0.56, market_probability: float = 0.51):
    edge = model_probability - market_probability
    return {'edge': edge}
