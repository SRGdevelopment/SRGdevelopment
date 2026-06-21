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
    assert payload
    assert all(market["is_live"] is True for market in payload)
