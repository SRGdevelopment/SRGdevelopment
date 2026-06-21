from fastapi.testclient import TestClient

from apps.api.src.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_live_markets_endpoint():
    response = client.get("/markets/live")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert {market["id"] for market in payload} == {"mkt_nba_001", "mkt_nba_002"}
