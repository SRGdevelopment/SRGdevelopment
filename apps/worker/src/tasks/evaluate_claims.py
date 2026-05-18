from ..celery_app import celery_app


@celery_app.task
def evaluate_claims(extracted: dict | None = None):
    payload = extracted or {'claims': []}
    evaluations = []
    for claim in payload.get('claims', []):
        confidence = claim.get('confidence_extract', 0.5)
        status = 'supported' if confidence > 0.75 else 'uncertain'
        evaluations.append({'claim_text': claim.get('claim_text', ''), 'status': status, 'confidence': confidence})
    return {'evaluations': evaluations}
