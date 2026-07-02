from datetime import UTC, datetime
from decimal import Decimal

from app.core.cache import TTLCache
from app.providers.base import (
    ProviderQuote,
    QuoteProvider,
    QuoteProviderError,
    QuoteRequest,
)
from app.providers.service import QuoteProviderService


class FailingProvider(QuoteProvider):
    name = "failing"

    def can_quote(self, request: QuoteRequest) -> bool:
        return True

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        raise QuoteProviderError("boom")


class WorkingProvider(QuoteProvider):
    name = "working"

    def __init__(self) -> None:
        self.calls = 0

    def can_quote(self, request: QuoteRequest) -> bool:
        return True

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        self.calls += 1
        return ProviderQuote(
            provider=self.name,
            token_in=request.token_in,
            token_out=request.token_out,
            amount_in=request.amount_in,
            amount_out=Decimal("2"),
            estimated_gas=100000,
            price_impact=Decimal("0.01"),
            route=["working route"],
            timestamp=datetime.now(UTC),
            warnings=[],
        )


def _request() -> QuoteRequest:
    return QuoteRequest(
        chain_id=1,
        token_in="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        token_out="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        amount_in=Decimal("1"),
        slippage_bps=50,
    )


def test_provider_fallback() -> None:
    working_provider = WorkingProvider()
    service = QuoteProviderService(
        providers=[FailingProvider(), working_provider],
        cache=TTLCache[ProviderQuote](ttl_seconds=0),
    )

    quote = service.get_quote(_request())

    assert quote.provider == "working"
    assert working_provider.calls == 1
    assert quote.warnings == ["failing: boom"]


def test_quote_cache_reuses_provider_response() -> None:
    working_provider = WorkingProvider()
    service = QuoteProviderService(
        providers=[working_provider],
        cache=TTLCache[ProviderQuote](ttl_seconds=10),
    )

    first = service.get_quote(_request())
    second = service.get_quote(_request())

    assert first is second
    assert working_provider.calls == 1
