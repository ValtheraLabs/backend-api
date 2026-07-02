from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_portfolio_returns_typed_mock_payload() -> None:
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

    response = client.get(f"/v1/portfolio/{address}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["wallet_address"] == address
    assert payload["chain_id"] == 1
    assert payload["total_value_usd"] == 6125.0
    assert payload["allocation_percent"] == 100.0
    assert payload["risk_flags"] == ["mock_data"]
    assert payload["updated_at"]
    assert payload["is_mock"] is True
    assert len(payload["assets"]) == 3
    assert payload["assets"][0]["allocation_percent"] == 71.43


def test_get_portfolio_rejects_invalid_evm_address() -> None:
    response = client.get("/v1/portfolio/0x123")

    assert response.status_code == 422
