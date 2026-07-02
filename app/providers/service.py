import json
from decimal import Decimal

from app.core.cache import TTLCache
from app.core.config import settings
from app.providers.base import (
    ProviderQuote,
    QuoteProvider,
    QuoteProviderError,
    QuoteRequest,
)
from app.providers.registry import get_default_providers


class QuoteProviderService:
    def __init__(
        self,
        providers: list[QuoteProvider] | None = None,
        cache: TTLCache[ProviderQuote] | None = None,
    ) -> None:
        self.providers = providers or get_default_providers()
        self.cache = cache or TTLCache[ProviderQuote](settings.quote_cache_ttl)

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        cache_key = self._cache_key(request)
        cached_quote = self.cache.get(cache_key)
        if cached_quote is not None:
            return cached_quote

        errors: list[str] = []
        for provider in self.providers:
            if not provider.can_quote(request):
                continue
            try:
                quote = provider.get_quote(request)
                if errors:
                    quote.warnings.extend(errors)
                self.cache.set(cache_key, quote)
                return quote
            except QuoteProviderError as exc:
                errors.append(f"{provider.name}: {exc}")

        raise QuoteProviderError(
            "No quote provider could produce a quote. " + " ".join(errors)
        )

    @staticmethod
    def _cache_key(request: QuoteRequest) -> str:
        payload = request.model_dump(mode="json")
        if isinstance(payload["amount_in"], Decimal):
            payload["amount_in"] = str(payload["amount_in"])
        return json.dumps(payload, sort_keys=True)
