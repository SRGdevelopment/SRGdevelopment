from fastapi.testclient import TestClient

from apps.api.src.main import app


client = TestClient(app)


def test_engine_bay_manifest_contract():
    response = client.get("/engine-bay/assemblies/srg-demo-engine-bay/asset-manifest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["assembly_id"] == "srg-demo-engine-bay"
    assert payload["draco_compressed"] is True
    assert payload["meshopt_compressed"] is True
    assert len(payload["parts"]) >= 4
    assert {part["id"] for part in payload["parts"]} >= {"intake_manifold", "turbocharger"}


def test_engine_bay_annotation_round_trip():
    response = client.post(
        "/engine-bay/assemblies/srg-demo-engine-bay/annotations",
        json={"part_id": "turbocharger", "note": "Oil feed line requires inspection", "severity": "warning"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["assembly_id"] == "srg-demo-engine-bay"
    assert payload["part_id"] == "turbocharger"
    assert payload["severity"] == "warning"


def test_engine_bay_unknown_assembly_returns_404():
    response = client.get("/engine-bay/assemblies/not-real/parts")

    assert response.status_code == 404
