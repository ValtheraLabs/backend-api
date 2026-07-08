import json
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import ANY, MagicMock, patch

import httpx
import pytest
from pytest import MonkeyPatch

from app.providers.base import QuoteProviderError, QuoteRequest
from app.providers.zerox import ZeroXProvider


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
    provider = ZeroXProvider(api_key="test-key")
    assert provider.can_quote(_request(chain_id=1))
    assert provider.can_quote(_request(chain_id=10))
    assert provider.can_quote(_request(chain_id=137))
    assert provider.can_quote(_request(chain_id=42161))
    assert provider.can_quote(_request(chain_id=8453))


def test_cannot_quote_unsupported_chain() -> None:
    provider = ZeroXProvider(api_key="test-key")
    assert not provider.can_quote(_request(chain_id=999))
    assert not provider.can_quote(_request(chain_id=56))


def test_get_quote_returns_provider_quote_on_success(
    monkeypatch: MonkeyPatch,
) -> None:
    fake_response = {
        "price": "1800.50",
        "buyAmount": "2700750000000000000000",
        "estimatedGas": "145000",
        "gasPrice": "25000000000",
        "sources": [{"name": "Uniswap_V3"}, {"name": "SushiSwap"}],
    }

    def mock_get(url: str, **kwargs: object) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = fake_response
        resp.raise_for_status = MagicMock()
        return resp

    monkeypatch.setattr("httpx.get", mock_get)

    provider = ZeroXProvider(api_key="test-key")
    quote = provider.get_quote(_request())

    assert quote.provider == "0x-api"
    assert quote.amount_in == Decimal("1.5")
    assert quote.amount_out == Decimal("2700.75")
    assert quote.estimated_gas == 145000
    assert "Uniswap_V3" in str(quote.route)
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

    provider = ZeroXProvider(api_key="test-key")
    with pytest.raises(QuoteProviderError, match="0x API returned error"):
        provider.get_quote(_request())


def test_get_quote_raises_on_network_error(monkeypatch: MonkeyPatch) -> None:
    def mock_get(url: str, **kwargs: object) -> MagicMock:
        raise httpx.ConnectError("connection refused", request=MagicMock())

    monkeypatch.setattr("httpx.get", mock_get)

    provider = ZeroXProvider(api_key="test-key")
    with pytest.raises(QuoteProviderError, match="0x API request failed"):
        provider.get_quote(_request())


def test_get_quote_includes_api_key_header(monkeypatch: MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def mock_get(url: str, **kwargs: object) -> MagicMock:
        captured["url"] = url
        captured["headers"] = kwargs.get("headers")
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = {
            "price": "1.0",
            "buyAmount": "1000000000000000000",
            "estimatedGas": "100000",
            "gasPrice": "10000000000",
            "sources": [{"name": "Test"}],
        }
        resp.raise_for_status = MagicMock()
        return resp

    monkeypatch.setattr("httpx.get", mock_get)

    provider = ZeroXProvider(api_key="sk-test-api-key-123")
    provider.get_quote(_request())

    assert "api.0x.org" in str(captured["url"])
    assert captured["headers"] is not None
    headers = captured["headers"]
    assert isinstance(headers, dict)
    assert headers.get("0x-api-key") == "sk-test-api-key-123"


def test_get_quote_raises_when_no_api_key_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.core.config.settings.zerox_api_key", "")
    provider = ZeroXProvider(api_key=None)
    with pytest.raises(QuoteProviderError, match="0x API key not configured"):
        provider.get_quote(_request())
