from fastapi import APIRouter

from ...schemas.integrity import IntegrityReport
from ...services.integrity_service import IntegrityService

router = APIRouter()
service = IntegrityService()


@router.get("/{market_id}/report", response_model=IntegrityReport)
def get_integrity_report(market_id: str):
    return service.analyze_market(market_id)
