from typing import Annotated

from fastapi import APIRouter, Path

from app.schemas.portfolio import PortfolioResponse
from app.services.portfolio_service import get_mock_portfolio

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

EVM_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"


@router.get("/{address}", response_model=PortfolioResponse)
def get_portfolio(
    address: Annotated[
        str,
        Path(
            ...,
            description="EVM wallet address in 0x-prefixed 40-byte hex format.",
            pattern=EVM_ADDRESS_PATTERN,
            examples=["0x742d35Cc6634C0532925a3b844Bc454e4438f44e"],
        ),
    ],
) -> PortfolioResponse:
    return get_mock_portfolio(address)
