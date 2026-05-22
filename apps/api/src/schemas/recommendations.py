from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    market_id: str
    side: str = Field(pattern="^(A|B)$")
    edge: float
    value_score: float
    recommended_stake_fraction: float = Field(ge=0, le=1)


class TopRecommendationsResponse(BaseModel):
    recommendations: list[Recommendation]
