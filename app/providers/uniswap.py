from datetime import UTC, datetime
from decimal import ROUND_DOWN, Decimal

from app.providers.base import ProviderQuote, QuoteProvider, QuoteRequest


class UniswapV3QuoterProvider(QuoteProvider):
    name = "uniswap-v3-quoter"
    _mock_rate = Decimal("1800")

    def can_quote(self, request: QuoteRequest) -> bool:
        return request.chain_id == 1

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        amount_out = (request.amount_in * self._mock_rate).quantize(
            Decimal("0.000001"),
            rounding=ROUND_DOWN,
        )
        return ProviderQuote(
            provider=self.name,
            token_in=request.token_in,
            token_out=request.token_out,
            amount_in=request.amount_in,
            amount_out=amount_out,
            estimated_gas=150000,
            price_impact=Decimal("0.12"),
            route=["Uniswap V3 Quoter", "Mock pool path"],
            timestamp=datetime.now(UTC),
            warnings=[
                "Quote-only provider stub. No transaction has been built.",
                (
                    "Live RPC integration will be added after provider "
                    "credentials are configured."
                ),
            ],
        )
