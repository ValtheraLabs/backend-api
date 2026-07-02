from datetime import UTC, datetime
from decimal import Decimal, ROUND_DOWN

from app.schemas.quote import QuoteResponse, QuoteRouteStep

MOCK_PROVIDER = "valthera-mock-quote-engine"
MOCK_RATE = Decimal("1800")


def get_mock_quote(
    chain_id: int,
    token_in: str,
    token_out: str,
    amount_in: Decimal,
    slippage_bps: int,
) -> QuoteResponse:
    amount_out = (amount_in * MOCK_RATE).quantize(
        Decimal("0.000001"),
        rounding=ROUND_DOWN,
    )

    return QuoteResponse(
        chain_id=chain_id,
        token_in=token_in,
        token_out=token_out,
        amount_in=amount_in,
        amount_out_estimate=amount_out,
        price_impact_percent=Decimal("0.12"),
        slippage_bps=slippage_bps,
        route=[
            QuoteRouteStep(
                label="Mock direct route",
                provider=MOCK_PROVIDER,
                token_in=token_in,
                token_out=token_out,
            )
        ],
        gas_estimate=150000,
        provider=MOCK_PROVIDER,
        warnings=[
            "Mock quote only. No DEX routing has been performed.",
            "No transaction has been built, signed, or submitted.",
        ],
        updated_at=datetime.now(UTC),
    )
