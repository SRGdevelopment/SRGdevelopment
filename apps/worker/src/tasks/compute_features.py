from ..celery_app import celery_app


@celery_app.task
def compute_features(market_snapshot: dict | None = None):
    snapshot = market_snapshot or {'liquidity': 0.7, 'volatility': 0.2, 'momentum': 0.1}
    uncertainty = max(0.0, min(1.0, 0.6 * snapshot['volatility'] + 0.4 * abs(snapshot['momentum'])))
    return {
        'liquidity': snapshot['liquidity'],
        'volatility': snapshot['volatility'],
        'momentum': snapshot['momentum'],
        'uncertainty': uncertainty,
    }
