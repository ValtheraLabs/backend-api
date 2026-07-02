from decimal import Decimal

from app.providers.base import QuoteProviderError, QuoteRequest
from app.providers.service import QuoteProviderService
from app.schemas.quote import QuoteResponse

quote_provider_service = QuoteProviderService()


def get_quote(
    chain_id: int,
    token_in: str,
    token_out: str,
    amount_in: Decimal,
    slippage_bps: int,
) -> QuoteResponse:
    provider_quote = quote_provider_service.get_quote(
        QuoteRequest(
            chain_id=chain_id,
            token_in=token_in,
            token_out=token_out,
            amount_in=amount_in,
            slippage_bps=slippage_bps,
        )
    )
    return QuoteResponse(
        provider=provider_quote.provider,
        chain_id=chain_id,
        token_in=provider_quote.token_in,
        token_out=provider_quote.token_out,
        amount_in=provider_quote.amount_in,
        amount_out=provider_quote.amount_out,
        estimated_gas=provider_quote.estimated_gas,
        price_impact=provider_quote.price_impact,
        slippage_bps=slippage_bps,
        route=provider_quote.route,
        timestamp=provider_quote.timestamp,
        warnings=provider_quote.warnings,
    )


__all__ = ["QuoteProviderError", "get_quote", "quote_provider_service"]
