from pydantic import BaseModel, Field
from typing import List


class IntegritySignal(BaseModel):
    code: str
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    description: str


class IntegrityReport(BaseModel):
    market_id: str
    risk_score: float = Field(ge=0, le=1)
    signals: List[IntegritySignal]
    summary: str
