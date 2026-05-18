from fastapi import APIRouter

from ...schemas.recommendations import TopRecommendationsResponse
from ...services.recommendation_service import RecommendationService

router = APIRouter()
service = RecommendationService()


@router.get('/top', response_model=TopRecommendationsResponse)
def list_top_recommendations():
    return TopRecommendationsResponse(recommendations=service.top_recommendations())
