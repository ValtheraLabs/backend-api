import json
from collections.abc import Callable

import httpx
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.main import app
from app.services import ai_client

client = TestClient(app)


def _mock_ai_engine(
    monkeypatch: MonkeyPatch,
    handler: Callable[[httpx.Request], httpx.Response],
) -> None:
    transport = httpx.MockTransport(handler)

    def create_http_client() -> httpx.Client:
        return httpx.Client(
            base_url="http://ai-engine.test",
            transport=transport,
            timeout=5,
        )

    monkeypatch.setattr(ai_client, "_create_http_client", create_http_client)


def test_analyze_portfolio_uses_ai_engine(monkeypatch: MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.method == "POST"
        assert request.url.path == "/v1/analyze/portfolio"
        assert body["wallet_address"] == "0x123"
        assert body["chain_id"] == 1
        assert body["assets"] == []
        return httpx.Response(
            200,
            json={
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
                "disclaimer": (
                    "Mock analysis for product development only. "
                    "This is not financial advice."
                ),
            },
        )

    _mock_ai_engine(monkeypatch, handler)

    response = client.post(
        "/api/v1/ai/analyze-portfolio",
        json={"address": "0x123", "chain_id": 1},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["source"] == "ai-engine"
    assert payload["analysis_id"] == "mock-portfolio-analysis"
    assert payload["risk_score"] == 38
    assert payload["insights"][0]["category"] == "Data completeness"


def test_analyze_token_uses_ai_engine(monkeypatch: MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.method == "POST"
        assert request.url.path == "/v1/analyze/token"
        assert body["token_address"] == "0xabc"
        assert body["symbol"] == "VAL"
        return httpx.Response(
            200,
            json={
                "analysis_id": "mock-token-analysis",
                "token_symbol": "VAL",
                "summary": "Structured mock token analysis completed for VAL.",
                "risk_score": 55,
                "confidence": "low",
                "risk_factors": [
                    {
                        "name": "Liquidity",
                        "severity": "medium",
                        "explanation": "Liquidity depth is not connected yet.",
                    }
                ],
                "recommended_actions": [
                    {
                        "label": "Verify token data",
                        "rationale": (
                            "Review trusted market sources before making decisions."
                        ),
                        "priority": "high",
                    }
                ],
                "disclaimer": (
                    "Mock analysis for product development only. "
                    "This is not financial advice."
                ),
            },
        )

    _mock_ai_engine(monkeypatch, handler)

    response = client.post(
        "/api/v1/ai/analyze-token",
        json={"token_address": "0xabc", "chain_id": 1, "symbol": "VAL"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["source"] == "ai-engine"
    assert payload["symbol"] == "VAL"
    assert payload["risk_level"] == "low"
    assert payload["recommended_actions"][0]["priority"] == "high"


def test_analyze_token_returns_clear_error_when_ai_engine_unavailable(
    monkeypatch: MonkeyPatch,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    _mock_ai_engine(monkeypatch, handler)

    response = client.post(
        "/api/v1/ai/analyze-token",
        json={"token_address": "0xabc", "chain_id": 1, "symbol": "VAL"},
    )

    payload = response.json()
    assert response.status_code == 503
    assert payload == {
        "error": "ai_engine_unavailable",
        "message": "AI engine is unavailable.",
    }
    assert "ai_engine_base_url" not in payload


def test_analyze_portfolio_returns_clear_error_on_ai_engine_timeout(
    monkeypatch: MonkeyPatch,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    _mock_ai_engine(monkeypatch, handler)

    response = client.post(
        "/api/v1/ai/analyze-portfolio",
        json={"address": "0x123", "chain_id": 1},
    )

    payload = response.json()
    assert response.status_code == 503
    assert payload["error"] == "ai_engine_unavailable"
    assert payload["message"] == "AI engine request timed out."
    assert "ai_engine_base_url" not in payload
