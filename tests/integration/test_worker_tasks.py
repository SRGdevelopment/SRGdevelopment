from apps.worker.src.tasks.compute_edges import compute_edges
from apps.worker.src.tasks.compute_features import compute_features
from apps.worker.src.tasks.detect_mispricing import detect_mispricing
from apps.worker.src.tasks.evaluate_claims import evaluate_claims
from apps.worker.src.tasks.extract_claims import extract_claims
from apps.worker.src.tasks.ingest_markets import ingest_markets
from apps.worker.src.tasks.ingest_media import ingest_media
from apps.worker.src.tasks.ingest_sports_context import ingest_sports_context
from apps.worker.src.tasks.monitor_integrity import monitor_integrity
from apps.worker.src.tasks.run_predictions import run_predictions


def test_ingest_markets_returns_market_payload():
    result = ingest_markets.run()

    assert len(result["markets"]) == 2
    assert result["markets"][0]["id"] == "mkt_nba_001"


def test_claim_pipeline_tasks():
    extracted = extract_claims.run("Team X is 8-1 on back-to-backs this season.")
    evaluations = evaluate_claims.run(extracted)

    assert extracted["claims"][0]["league"] == "NBA"
    assert evaluations["evaluations"][0]["status"] == "supported"


def test_feature_prediction_and_edge_pipeline():
    features = compute_features.run({"liquidity": 0.7, "volatility": 0.2, "momentum": 0.1})
    prediction = run_predictions.run(features)
    edge = compute_edges.run(prediction["model_probability"], 0.51)

    assert 0 <= features["uncertainty"] <= 1
    assert 0.01 <= prediction["model_probability"] <= 0.99
    assert edge["edge"] > 0


def test_ingest_media_and_context_tasks():
    media = ingest_media.run("podcast", "Line movement looks suspicious tonight.")
    context = ingest_sports_context.run("NBA")

    assert media["status"] == "queued"
    assert context["league"] == "NBA"
    assert context["items"]


def test_detect_mispricing_and_monitor_integrity():
    report = detect_mispricing.run()
    integrity = monitor_integrity.run()

    assert report["action"] == "consider_buy"
    assert integrity == "integrity monitor executed"
