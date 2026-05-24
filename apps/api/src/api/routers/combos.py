from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ...schemas.recommendations import Recommendation
from ...services.recommendation_service import RecommendationService

router = APIRouter()
service = RecommendationService()


class ComboLeg(BaseModel):
    market_id: str
    side: str = Field(pattern="^(A|B)$")
    edge: float
    recommended_stake_fraction: float = Field(ge=0, le=1)
    recommended_stake_amount: float = Field(ge=0)


class ComboRequest(BaseModel):
    bankroll: float = Field(default=100.0, gt=0)
    max_legs: int = Field(default=2, ge=1, le=5)
    include_market_ids: list[str] = Field(default_factory=list)


class ComboTweakRequest(ComboRequest):
    locked_market_ids: list[str] = Field(default_factory=list)
    excluded_market_ids: list[str] = Field(default_factory=list)


class ComboResponse(BaseModel):
    legs: list[ComboLeg]
    total_edge: float
    total_stake_fraction: float = Field(ge=0, le=1)
    total_stake_amount: float = Field(ge=0)
    rationale: str


def _to_combo_leg(recommendation: Recommendation, bankroll: float) -> ComboLeg:
    stake_amount = round(bankroll * recommendation.recommended_stake_fraction, 2)
    return ComboLeg(
        market_id=recommendation.market_id,
        side=recommendation.side,
        edge=recommendation.edge,
        recommended_stake_fraction=recommendation.recommended_stake_fraction,
        recommended_stake_amount=stake_amount,
    )


def _pick_recommendations(
    bankroll: float,
    max_legs: int,
    include_market_ids: list[str] | None = None,
    locked_market_ids: list[str] | None = None,
    excluded_market_ids: list[str] | None = None,
) -> ComboResponse:
    available = service.top_recommendations()
    include = set(include_market_ids or [])
    locked = set(locked_market_ids or [])
    excluded = set(excluded_market_ids or [])
    selected: list[Recommendation] = []
    selected_ids: set[str] = set()

    for recommendation in available:
        if recommendation.market_id in locked and recommendation.market_id not in excluded:
            selected.append(recommendation)
            selected_ids.add(recommendation.market_id)

    filtered = [
        recommendation
        for recommendation in available
        if recommendation.market_id not in selected_ids
        and recommendation.market_id not in excluded
        and (not include or recommendation.market_id in include)
    ]
    selected.extend(filtered[: max(0, max_legs - len(selected))])

    if not selected:
        raise HTTPException(status_code=404, detail="No eligible combo recommendations found")

    legs = [_to_combo_leg(recommendation, bankroll) for recommendation in selected[:max_legs]]
    total_edge = round(sum(leg.edge for leg in legs), 4)
    total_stake_fraction = round(sum(leg.recommended_stake_fraction for leg in legs), 4)
    total_stake_amount = round(sum(leg.recommended_stake_amount for leg in legs), 2)
    rationale = f"Selected {len(legs)} highest-value recommendations after combo filters."
    return ComboResponse(
        legs=legs,
        total_edge=total_edge,
        total_stake_fraction=total_stake_fraction,
        total_stake_amount=total_stake_amount,
        rationale=rationale,
    )


@router.post("/generate", response_model=ComboResponse)
def generate_combo(payload: ComboRequest):
    return _pick_recommendations(
        bankroll=payload.bankroll,
        max_legs=payload.max_legs,
        include_market_ids=payload.include_market_ids,
    )


@router.post("/tweak", response_model=ComboResponse)
def tweak_combo(payload: ComboTweakRequest):
    return _pick_recommendations(
        bankroll=payload.bankroll,
        max_legs=payload.max_legs,
        include_market_ids=payload.include_market_ids,
        locked_market_ids=payload.locked_market_ids,
        excluded_market_ids=payload.excluded_market_ids,
    )
