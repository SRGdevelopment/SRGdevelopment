from ..celery_app import celery_app


@celery_app.task
def run_predictions(features: dict | None = None):
    f = features or {'liquidity': 0.7, 'volatility': 0.2, 'momentum': 0.1, 'uncertainty': 0.16}
    p_model = 0.5 + 0.25 * f['momentum'] + 0.1 * f['liquidity'] - 0.2 * f['volatility']
    p_model = max(0.01, min(0.99, p_model))
    return {'model_probability': p_model, 'features': f}
