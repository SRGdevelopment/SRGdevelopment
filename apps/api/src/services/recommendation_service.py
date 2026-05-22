from ..schemas.recommendations import Recommendation
from .pricing_service import PricingService


class RecommendationService:
    def __init__(self) -> None:
        self.pricing = PricingService()

    def _kelly_fraction(self, p_model: float, p_market: float, cap: float = 0.05) -> float:
        b = (1 / p_market) - 1 if p_market > 0 else 0
        q = 1 - p_model
        raw = max(0.0, (b * p_model - q) / b) if b > 0 else 0.0
        return min(raw * 0.5, cap)

    def top_recommendations(self) -> list[Recommendation]:
        samples = [
            ("mkt_nba_001", "A", 0.61, 54, 0.84, 0.78, 0.22, 0.12),
            ("mkt_nba_002", "B", 0.58, 51, 0.72, 0.71, 0.30, 0.18),
            ("mkt_nba_003", "A", 0.55, 57, 0.67, 0.40, 0.38, 0.26),
        ]
        recs: list[Recommendation] = []
        for market_id, side, p_model, price, confidence, liquidity, volatility, uncertainty in samples:
            p_market = self.pricing.implied_probability_from_cents(price)
            edge = p_model - p_market
            value = 0.55 * edge + 0.20 * liquidity - 0.15 * volatility - 0.10 * uncertainty
            if confidence < 0.6 or value <= 0:
                continue
            stake = self._kelly_fraction(p_model, p_market)
            recs.append(Recommendation(market_id=market_id, side=side, edge=edge, value_score=value, recommended_stake_fraction=stake))
        return sorted(recs, key=lambda r: r.value_score, reverse=True)
