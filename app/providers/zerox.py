from app.providers.base import (
    ProviderQuote,
    QuoteProvider,
    QuoteProviderError,
    QuoteRequest,
)


class ZeroXProvider(QuoteProvider):
    name = "0x-api"

    def can_quote(self, request: QuoteRequest) -> bool:
        return request.chain_id in {1, 10, 137, 42161, 8453}

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        raise QuoteProviderError("0x API is not configured for live quotes.")
