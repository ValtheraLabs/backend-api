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

ONEINCH_BASE_URL = "https://api.1inch.dev"

SUPPORTED_CHAINS = {1, 10, 56, 137, 42161, 8453}


class OneInchProvider(QuoteProvider):
    name = "1inch"

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or settings.oneinch_api_key

    def can_quote(self, request: QuoteRequest) -> bool:
        return request.chain_id in SUPPORTED_CHAINS

    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        if not self._api_key:
            raise QuoteProviderError("1inch API key not configured. Set ONEINCH_API_KEY.")

        api_url = f"{ONEINCH_BASE_URL}/swap/v5.2/{request.chain_id}/quote"
        params: dict[str, str | int] = {
            "src": request.token_in,
            "dst": request.token_out,
            "amount": str(int(request.amount_in * Decimal("1e18"))),
            "slippage": str(request.slippage_bps),
        }

        try:
            response = httpx.get(
                api_url,
                params=params,
                headers={"Authorization": f"Bearer {self._api_key}"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            raise QuoteProviderError(
                f"1inch API returned error {exc.response.status_code}"
            ) from exc
        except httpx.TimeoutException as exc:
            raise QuoteProviderError("1inch API request timed out.") from exc
        except httpx.RequestError as exc:
            raise QuoteProviderError(
                f"1inch API request failed: {exc}"
            ) from exc

        amount_out = self._decode_amount(data.get("toAmount", "0"))
        estimated_gas = int(data.get("estimatedGas", 0))

        return ProviderQuote(
            provider=self.name,
            token_in=request.token_in,
            token_out=request.token_out,
            amount_in=request.amount_in,
            amount_out=amount_out,
            estimated_gas=estimated_gas,
            price_impact=Decimal("0"),
            route=["1inch route"],
            timestamp=datetime.now(UTC),
            warnings=[],
        )

    @staticmethod
    def _decode_amount(raw: str) -> Decimal:
        try:
            return Decimal(raw) / Decimal("1e18")
        except Exception:
            return Decimal("0")
