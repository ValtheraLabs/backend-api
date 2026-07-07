from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from app.schemas.portfolio import PortfolioResponse
from app.services.portfolio_service import get_portfolio, _validate_address


def test_validate_address_rejects_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid Ethereum address"):
        _validate_address("0x123")


def test_validate_address_rejects_empty() -> None:
    with pytest.raises(ValueError, match="Invalid Ethereum address"):
        _validate_address("")


def test_validate_address_accepts_valid() -> None:
    _validate_address("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")


def test_get_portfolio_uses_provided_rpc(monkeypatch: MonkeyPatch) -> None:
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

    portfolio = get_portfolio(
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        rpc_url="https://eth-mainnet.g.alchemy.com/v2/test",
    )

    assert isinstance(portfolio, PortfolioResponse)
    assert portfolio.is_mock is False
    assert any(a.symbol == "ETH" for a in portfolio.assets)
    eth = next(a for a in portfolio.assets if a.symbol == "ETH")
    assert eth.balance == "2.5000"
    assert eth.value_usd > 0


def test_get_portfolio_handles_rpc_failure(monkeypatch: MonkeyPatch) -> None:
    mock_w3 = MagicMock()
    mock_w3.is_connected.return_value = False

    mock_web3_cls = MagicMock()
    mock_web3_cls.is_address.return_value = True
    mock_web3_cls.HTTPProvider.return_value = "mock-provider"
    mock_web3_cls.return_value = mock_w3

    monkeypatch.setattr("app.services.portfolio_service.Web3", mock_web3_cls)

    with pytest.raises(RuntimeError, match="Unable to connect to RPC"):
        get_portfolio(
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            rpc_url="https://eth-mainnet.g.alchemy.com/v2/test",
        )
