from fastapi.testclient import TestClient

from apps.api.src.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_live_markets():
    response = client.get("/markets/live")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {market["id"] for market in body} == {"mkt_nba_001", "mkt_nba_002"}


def test_market_not_found():
    response = client.get("/markets/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Market not found"


def test_get_mispricing_report():
    response = client.get(
        "/markets/mkt_nba_001/mispricing",
        params={"model_probability": 0.61, "price_cents": 54, "confidence": 0.84},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["action"] == "consider_buy"
    assert body["market_id"] == "mkt_nba_001"


def test_top_recommendations():
    response = client.get("/recommendations/top")

    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"]
    assert body["recommendations"][0]["market_id"] == "mkt_nba_001"


def test_generate_combo():
    response = client.post("/combos/generate", json={"bankroll": 200, "max_legs": 2})

    assert response.status_code == 200
    body = response.json()
    assert len(body["legs"]) == 2
    assert body["total_stake_amount"] > 0


def test_tweak_combo_respects_filters():
    response = client.post(
        "/combos/tweak",
        json={
            "bankroll": 100,
            "max_legs": 2,
            "locked_market_ids": ["mkt_nba_002"],
            "excluded_market_ids": ["mkt_nba_001"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["legs"][0]["market_id"] == "mkt_nba_002"
    assert all(leg["market_id"] != "mkt_nba_001" for leg in body["legs"])


def test_media_ingest_and_claim_lookup():
    response = client.post(
        "/media/ingest",
        json={"source": "podcast", "content": "Team X is 8-1 on back-to-backs."},
    )

    assert response.status_code == 200
    media_id = response.json()["media_id"]

    claims_response = client.get(f"/media/{media_id}/claims")
    assert claims_response.status_code == 200
    assert claims_response.json()["id"] == media_id


def test_claim_evaluation_not_found():
    response = client.get("/claims/unknown/evaluation")

    assert response.status_code == 404
    assert response.json()["detail"] == "Claim evaluation not found"


def test_integrity_report():
    response = client.get("/integrity/mkt_nba_001/report")

    assert response.status_code == 200
    body = response.json()
    assert body["market_id"] == "mkt_nba_001"
    assert body["signals"]
