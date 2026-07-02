from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

TOKEN_IN = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
TOKEN_OUT = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"


def test_get_quote_returns_typed_mock_payload() -> None:
    response = client.get(
        "/v1/quote",
        params={
            "chain_id": 1,
            "token_in": TOKEN_IN,
            "token_out": TOKEN_OUT,
            "amount_in": "1.5",
            "slippage_bps": 50,
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["chain_id"] == 1
    assert payload["token_in"] == TOKEN_IN
    assert payload["token_out"] == TOKEN_OUT
    assert payload["amount_in"] == "1.5"
    assert payload["amount_out_estimate"] == "2700.000000"
    assert payload["price_impact_percent"] == "0.12"
    assert payload["slippage_bps"] == 50
    assert payload["route"][0]["provider"] == "valthera-mock-quote-engine"
    assert payload["gas_estimate"] == 150000
    assert payload["provider"] == "valthera-mock-quote-engine"
    assert payload["warnings"]
    assert payload["updated_at"]
    assert payload["is_mock"] is True


def test_get_quote_rejects_invalid_token_address() -> None:
    response = client.get(
        "/v1/quote",
        params={
            "chain_id": 1,
            "token_in": "0x123",
            "token_out": TOKEN_OUT,
            "amount_in": "1",
            "slippage_bps": 50,
        },
    )

    assert response.status_code == 422


def test_get_quote_rejects_invalid_amount() -> None:
    response = client.get(
        "/v1/quote",
        params={
            "chain_id": 1,
            "token_in": TOKEN_IN,
            "token_out": TOKEN_OUT,
            "amount_in": "0",
            "slippage_bps": 50,
        },
    )

    assert response.status_code == 422
