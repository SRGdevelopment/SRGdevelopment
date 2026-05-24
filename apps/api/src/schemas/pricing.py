from pydantic import BaseModel, ConfigDict, Field


class MispricingReport(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    market_id: str
    side: str = Field(pattern="^(A|B)$")
    model_probability: float = Field(ge=0, le=1)
    implied_probability: float = Field(ge=0, le=1)
    edge: float
    confidence: float = Field(ge=0, le=1)
    action: str
