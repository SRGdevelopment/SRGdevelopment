from pydantic import BaseModel, Field


class MarketOut(BaseModel):
    id: str
    event: str
    side_a_price_cents: int = Field(ge=1, le=99)
    side_b_price_cents: int = Field(ge=1, le=99)
    liquidity: float = Field(ge=0, le=1)
    volatility: float = Field(ge=0, le=1)
    is_live: bool
