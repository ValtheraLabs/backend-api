from fastapi.testclient import TestClient

from app.main import app
from app.services import ai_service


client = TestClient(app)


def test_analyze_portfolio_uses_ai_engine(monkeypatch) -> None:
    def fake_post(path: str, payload: dict) -> dict:
        assert path == "/v1/analyze/portfolio"
        assert payload["wallet_address"] == "0x123"
        return {
            "analysis_id": "mock-portfolio-analysis",
            "summary": "Structured mock portfolio analysis completed.",
            "risk_score": 38,
            "confidence": "medium",
            "risk_factors": [
                {
                    "name": "Data completeness",
                    "severity": "medium",
                    "explanation": "Mock explanation.",
                }
            ],
            "recommended_actions": [],
            "disclaimer": "Mock analysis for product development only. This is not financial advice.",
        }

    monkeypatch.setattr(ai_service, "_post_ai_engine", fake_post)

    response = client.post(
        "/v1/ai/analyze-portfolio",
        json={"address": "0x123", "chain_id": 1},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["source"] == "ai-engine"
    assert payload["analysis_id"] == "mock-portfolio-analysis"
    assert payload["risk_score"] == 38
    assert payload["insights"][0]["category"] == "Data completeness"


def test_analyze_token_falls_back_when_ai_engine_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(ai_service, "_post_ai_engine", lambda path, payload: None)

    response = client.post(
        "/v1/ai/analyze-token",
        json={"token_address": "0xabc", "chain_id": 1, "symbol": "VAL"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["source"] == "backend-fallback"
    assert payload["symbol"] == "VAL"
    assert payload["is_mock"] is True
