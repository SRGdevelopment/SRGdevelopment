from ..celery_app import celery_app


@celery_app.task
def extract_claims(media_text: str = ''):
    text = media_text or 'Team X is 8-1 on back-to-backs this season.'
    return {
        'claims': [
            {
                'claim_text': text,
                'entity_tags': ['Team X'],
                'metric': 'win_rate',
                'time_horizon': 'last_9_back_to_back_games',
                'league': 'NBA',
                'confidence_extract': 0.88,
            }
        ]
    }
