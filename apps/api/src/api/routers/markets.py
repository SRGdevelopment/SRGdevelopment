from fastapi import APIRouter, HTTPException, Query

from ...schemas.market import MarketOut
from ...schemas.pricing import MispricingReport
from ...services.market_service import MarketService
from ...services.pricing_service import PricingService

router = APIRouter()
service = PricingService()
market_service = MarketService()


@router.get('/live', response_model=list[MarketOut])
def list_live_markets():
    return market_service.list_live()


@router.get('/{market_id}', response_model=MarketOut)
def get_market(market_id: str):
    market = market_service.get(market_id)
    if market is None:
        raise HTTPException(status_code=404, detail='Market not found')
    return market


@router.get('/{market_id}/mispricing', response_model=MispricingReport)
def get_mispricing_report(
    market_id: str,
    side: str = Query('A', pattern='^(A|B)$'),
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
