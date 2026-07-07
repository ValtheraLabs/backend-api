from datetime import UTC, datetime
from decimal import Decimal

import httpx

from app.core.config import settings
from app.providers.base import (
    ProviderQuote,
    QuoteProvider,
    QuoteProviderError,
    QuoteRequest,
)

ZEROX_BASE_URL = "https://api.0x.org"

SUPPORTED_CHAINS: dict[int, str] = {
    1: "ethereum",
    10: "optimism",
    137: "polygon",
    42161: "arbitrum",
    8453: "base",
}


class ZeroXProvider(QuoteProvider):
    name = "0x-api"

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or settings.zerox_api_key

    def can_quote(self, request: QuoteRequest) -> bool:
        return request.chain_id in SUPPORTED_CHAINS

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        if not self._api_key:
            raise QuoteProviderError("0x API key not configured. Set ZEROX_API_KEY.")

        api_url = f"{ZEROX_BASE_URL}/swap/v1/quote"
        params: dict[str, str | int] = {
            "sellToken": request.token_in,
            "buyToken": request.token_out,
            "sellAmount": str(int(request.amount_in * Decimal("1e18"))),
            "slippageBps": request.slippage_bps,
        }

        try:
            response = httpx.get(
                api_url,
                params=params,
                headers={
                    "0x-api-key": self._api_key,
                    "0x-version": "v2",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            raise QuoteProviderError(
                f"0x API returned error {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except httpx.TimeoutException as exc:
            raise QuoteProviderError(
                "0x API request timed out."
            ) from exc
        except httpx.RequestError as exc:
            raise QuoteProviderError(
                f"0x API request failed: {exc}"
            ) from exc

        amount_out = self._decode_amount(data.get("buyAmount", "0"))
        estimated_gas = int(data.get("estimatedGas", 0))
        price_impact = Decimal(str(data.get("estimatedPriceImpact", "0")))
        sources = [s["name"] for s in data.get("sources", [])]

        return ProviderQuote(
            provider=self.name,
            token_in=request.token_in,
            token_out=request.token_out,
            amount_in=request.amount_in,
            amount_out=amount_out,
            estimated_gas=estimated_gas,
            price_impact=price_impact,
            route=sources or ["0x API route"],
            timestamp=datetime.now(UTC),
            warnings=[],
        )

    @staticmethod
    def _decode_amount(raw: str) -> Decimal:
        try:
            return Decimal(raw) / Decimal("1e18")
        except Exception:
            return Decimal("0")
