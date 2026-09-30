import os

os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_demo_document():
    response = client.post(
        "/generate",
        json={
            "document_type": "Non-Disclosure Agreement",
            "parties": "Alice (Disclosing Party), Example Ltd (Receiving Party)",
            "terms": "Protect confidential information; No disclosure without consent",
            "effective_date": "2026-09-28",
            "extra_instructions": "",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "NON-DISCLOSURE AGREEMENT" in data["content"]
    assert "Protect confidential information" in data["content"]
    assert data["demo_mode"] is True


def test_validation_rejects_missing_fields():
    response = client.post("/generate", json={"document_type": "NDA"})
    assert response.status_code == 422
