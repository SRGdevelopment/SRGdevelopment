from ..celery_app import celery_app


@celery_app.task
def ingest_markets():
    return {
        "markets": [
            {
                "id": "mkt_nba_001",
                "event": "BOS vs NYK",
                "side_a_price_cents": 54,
                "side_b_price_cents": 46,
                "liquidity": 0.78,
                "volatility": 0.22,
            },
            {
                "id": "mkt_nba_002",
                "event": "LAL vs DEN",
                "side_a_price_cents": 49,
                "side_b_price_cents": 51,
                "liquidity": 0.71,
                "volatility": 0.30,
            },
        ]
    }
