from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from app.main import app

client = TestClient(app)

VALID_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"


def _mock_web3(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_w3 = MagicMock()
    mock_w3.is_connected.return_value = True
    mock_w3.eth.get_balance.return_value = 2500000000000000000
    mock_w3.eth.contract.return_value.functions.balanceOf.return_value.call.return_value = 0
    mock_w3.eth.contract.return_value.functions.decimals.return_value.call.return_value = 18

    mock_web3_cls = MagicMock()
    mock_web3_cls.is_address.return_value = True
    mock_web3_cls.to_checksum_address.side_effect = lambda addr: addr
    mock_web3_cls.from_wei.side_effect = lambda wei, unit: float(wei) / 1e18
    mock_web3_cls.HTTPProvider.return_value = "mock-provider"
    mock_web3_cls.return_value = mock_w3

    monkeypatch.setattr("app.services.portfolio_service.Web3", mock_web3_cls)
    return mock_w3


def test_get_portfolio_returns_typed_payload(monkeypatch: MonkeyPatch) -> None:
    _mock_web3(monkeypatch)

    response = client.get(f"/v1/portfolio/{VALID_ADDRESS}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["wallet_address"] == VALID_ADDRESS
    assert payload["chain_id"] == 1
    assert payload["total_value_usd"] > 0
    assert payload["is_mock"] is False
    assert len(payload["assets"]) > 0


def test_get_portfolio_rejects_invalid_evm_address() -> None:
    response = client.get("/v1/portfolio/0x123")

    assert response.status_code == 422
