from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

_MEDIA = {'media_001': {'id': 'media_001', 'source': 'podcast', 'claims': ['claim_001', 'claim_002']}}


class MediaIngestRequest(BaseModel):
    source: str
    content: str


@router.post('/ingest')
def ingest_media(payload: MediaIngestRequest):
    media_id = f'media_{len(_MEDIA)+1:03d}'
    _MEDIA[media_id] = {'id': media_id, 'source': payload.source, 'claims': []}
    return {'media_id': media_id, 'status': 'queued'}


@router.get('/{media_id}/claims')
def get_media_claims(media_id: str):
    return _MEDIA.get(media_id, {'id': media_id, 'claims': []})
