from fastapi import APIRouter, HTTPException

router = APIRouter()

_CLAIM_EVALS = {
    'claim_001': {'claim_id': 'claim_001', 'status': 'supported', 'confidence': 0.81},
    'claim_002': {'claim_id': 'claim_002', 'status': 'mixed', 'confidence': 0.58},
}


@router.get('/{claim_id}/evaluation')
def get_claim_evaluation(claim_id: str):
    value = _CLAIM_EVALS.get(claim_id)
    if value is None:
        raise HTTPException(status_code=404, detail='Claim evaluation not found')
    return value
