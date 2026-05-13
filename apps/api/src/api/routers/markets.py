from fastapi import APIRouter, Query

from ...schemas.pricing import MispricingReport
from ...services.pricing_service import PricingService

router = APIRouter()
service = PricingService()


@router.get("/")
def list_markets():
    return {"message": "TODO: implement markets endpoints"}


@router.get("/{market_id}/mispricing", response_model=MispricingReport)
def get_mispricing_report(
    market_id: str,
    side: str = Query("A", pattern="^(A|B)$"),
    model_probability: float = Query(..., ge=0, le=1),
    price_cents: int = Query(..., ge=1, le=99),
    confidence: float = Query(..., ge=0, le=1),
):
    return service.mispricing_report(
        market_id=market_id,
        side=side,
        model_probability=model_probability,
        price_cents=price_cents,
        confidence=confidence,
    )
