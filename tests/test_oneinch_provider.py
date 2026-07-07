from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

import httpx
import pytest
from pytest import MonkeyPatch

from app.providers.base import QuoteProviderError, QuoteRequest
from app.providers.oneinch import OneInchProvider


def _request(**overrides: object) -> QuoteRequest:
    params: dict[str, object] = {
        "chain_id": 1,
        "token_in": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "amount_in": Decimal("1.5"),
        "slippage_bps": 50,
    }
    params.update(overrides)
    return QuoteRequest(**params)


def test_can_quote_supported_chain() -> None:
    provider = OneInchProvider(api_key="test-key")
    assert provider.can_quote(_request(chain_id=1))
    assert provider.can_quote(_request(chain_id=10))
    assert provider.can_quote(_request(chain_id=56))
    assert provider.can_quote(_request(chain_id=137))
    assert provider.can_quote(_request(chain_id=42161))
    assert provider.can_quote(_request(chain_id=8453))


def test_cannot_quote_unsupported_chain() -> None:
    provider = OneInchProvider(api_key="test-key")
    assert not provider.can_quote(_request(chain_id=999))


def test_get_quote_returns_provider_quote_on_success(
    monkeypatch: MonkeyPatch,
) -> None:
    fake_response = {
        "toAmount": "2700750000000000000000",
        "estimatedGas": 145000,
        "tx": {"from": "0xfrom", "to": "0xto", "data": "0x"},
    }

    def mock_get(url: str, **kwargs: object) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = fake_response
        resp.raise_for_status = MagicMock()
        return resp

    monkeypatch.setattr("httpx.get", mock_get)

    provider = OneInchProvider(api_key="test-key")
    quote = provider.get_quote(_request())

    assert quote.provider == "1inch"
    assert quote.amount_in == Decimal("1.5")
    assert quote.amount_out == Decimal("2700.75")
    assert quote.estimated_gas == 145000
    assert quote.warnings == []


def test_get_quote_raises_on_api_error(monkeypatch: MonkeyPatch) -> None:
    def mock_get(url: str, **kwargs: object) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 400
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request", request=MagicMock(), response=resp
        )
        return resp

    monkeypatch.setattr("httpx.get", mock_get)

    provider = OneInchProvider(api_key="test-key")
    with pytest.raises(QuoteProviderError, match="1inch API returned error"):
        provider.get_quote(_request())


def test_get_quote_raises_on_network_error(monkeypatch: MonkeyPatch) -> None:
    def mock_get(url: str, **kwargs: object) -> MagicMock:
        raise httpx.ConnectError("connection refused", request=MagicMock())

    monkeypatch.setattr("httpx.get", mock_get)

    provider = OneInchProvider(api_key="test-key")
    with pytest.raises(QuoteProviderError, match="1inch API request failed"):
        provider.get_quote(_request())


def test_get_quote_raises_when_no_api_key() -> None:
    provider = OneInchProvider(api_key="")
    with pytest.raises(QuoteProviderError, match="1inch API key not configured"):
        provider.get_quote(_request())
