from app.providers.base import (
    ProviderQuote,
    QuoteProvider,
    QuoteProviderError,
    QuoteRequest,
)


class OneInchProvider(QuoteProvider):
    name = "1inch"

    def can_quote(self, request: QuoteRequest) -> bool:
        return request.chain_id in {1, 10, 56, 137, 42161, 8453}

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        raise QuoteProviderError("1inch API is not configured for live quotes.")
