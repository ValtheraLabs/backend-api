from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_v1_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "backend-api"


def test_response_includes_request_id_header() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["x-request-id"]


def test_response_preserves_incoming_request_id_header() -> None:
    response = client.get(
        "/api/v1/health",
        headers={"x-request-id": "frontend-request-123"},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "frontend-request-123"
