from ..schemas.pricing import MispricingReport


class PricingService:
    """Detects potential false-odds opportunities from model vs market prices."""

    def implied_probability_from_cents(self, price_cents: int) -> float:
        return max(0.0, min(1.0, price_cents / 100.0))

    def mispricing_report(
        self,
        market_id: str,
        side: str,
        model_probability: float,
        price_cents: int,
        confidence: float,
    ) -> MispricingReport:
        implied = self.implied_probability_from_cents(price_cents)
        edge = model_probability - implied
        if confidence < 0.55:
            action = "hold_low_confidence"
        elif edge >= 0.05:
            action = "consider_buy"
        elif edge <= -0.05:
            action = "consider_sell_or_hedge"
        else:
            action = "no_trade"

        return MispricingReport(
            market_id=market_id,
            side=side,
            model_probability=model_probability,
            implied_probability=implied,
            edge=edge,
            confidence=confidence,
            action=action,
        )
