from fastapi import APIRouter

from app.schemas.portfolio import PortfolioResponse
from app.services.portfolio_service import get_mock_portfolio

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/{address}", response_model=PortfolioResponse)
def get_portfolio(address: str) -> PortfolioResponse:
    return get_mock_portfolio(address)
