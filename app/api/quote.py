from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.quote import QuoteResponse
from app.services.quote_service import get_mock_quote

router = APIRouter(prefix="/quote", tags=["quote"])

EVM_TOKEN_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"


@router.get("", response_model=QuoteResponse)
def get_quote(
    chain_id: Annotated[int, Query(..., ge=1)],
    token_in: Annotated[
        str,
        Query(
            ...,
            description="Input EVM token address in 0x-prefixed 40-byte hex format.",
            pattern=EVM_TOKEN_ADDRESS_PATTERN,
        ),
    ],
    token_out: Annotated[
        str,
        Query(
            ...,
            description="Output EVM token address in 0x-prefixed 40-byte hex format.",
            pattern=EVM_TOKEN_ADDRESS_PATTERN,
        ),
    ],
    amount_in: Annotated[Decimal, Query(..., gt=0)],
    slippage_bps: Annotated[int, Query(..., ge=0)],
) -> QuoteResponse:
    return get_mock_quote(
        chain_id=chain_id,
        token_in=token_in,
        token_out=token_out,
        amount_in=amount_in,
        slippage_bps=slippage_bps,
    )
