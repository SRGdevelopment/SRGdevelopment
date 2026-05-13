from pydantic import BaseModel, Field


class MispricingReport(BaseModel):
    market_id: str
    side: str = Field(pattern="^(A|B)$")
    model_probability: float = Field(ge=0, le=1)
    implied_probability: float = Field(ge=0, le=1)
    edge: float
    confidence: float = Field(ge=0, le=1)
    action: str
