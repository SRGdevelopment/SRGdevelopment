from ..celery_app import celery_app


@celery_app.task
def detect_mispricing(
    market_id: str = "mkt_nba_001",
    side: str = "A",
    model_probability: float = 0.61,
    market_price_cents: int = 54,
    confidence: float = 0.84,
):
    implied_probability = market_price_cents / 100.0
    edge = round(model_probability - implied_probability, 4)
    if confidence < 0.55:
        action = "hold_low_confidence"
    elif edge >= 0.05:
        action = "consider_buy"
    elif edge <= -0.05:
        action = "consider_sell_or_hedge"
    else:
        action = "no_trade"
    return {
        "market_id": market_id,
        "side": side,
        "model_probability": model_probability,
        "implied_probability": implied_probability,
        "edge": edge,
        "confidence": confidence,
        "action": action,
    }
