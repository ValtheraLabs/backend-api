from fastapi import APIRouter

from app.schemas.ai import (
    AnalyzePortfolioRequest,
    AnalyzePortfolioResponse,
    AnalyzeTokenRequest,
    AnalyzeTokenResponse,
)
from app.services.ai_service import analyze_portfolio, analyze_token

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze-portfolio", response_model=AnalyzePortfolioResponse)
def analyze_portfolio_endpoint(
    payload: AnalyzePortfolioRequest,
) -> AnalyzePortfolioResponse:
    return analyze_portfolio(payload)


@router.post("/analyze-token", response_model=AnalyzeTokenResponse)
def analyze_token_endpoint(payload: AnalyzeTokenRequest) -> AnalyzeTokenResponse:
    return analyze_token(payload)
