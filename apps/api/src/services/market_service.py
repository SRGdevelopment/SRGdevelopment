from ..schemas.market import MarketOut


class MarketService:
    def __init__(self) -> None:
        self._markets = [
            MarketOut(id="mkt_nba_001", event="BOS vs NYK", side_a_price_cents=54, side_b_price_cents=46, liquidity=0.78, volatility=0.22, is_live=True),
            MarketOut(id="mkt_nba_002", event="LAL vs DEN", side_a_price_cents=49, side_b_price_cents=51, liquidity=0.71, volatility=0.30, is_live=True),
            MarketOut(id="mkt_nba_003", event="MIA vs PHI", side_a_price_cents=57, side_b_price_cents=43, liquidity=0.40, volatility=0.38, is_live=False),
        ]

    def list_live(self) -> list[MarketOut]:
        return [m for m in self._markets if m.is_live]

    def get(self, market_id: str) -> MarketOut | None:
        return next((m for m in self._markets if m.id == market_id), None)
