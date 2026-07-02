from app.schemas.ai import (
    AnalyzePortfolioRequest,
    AnalyzePortfolioResponse,
    AnalyzeTokenRequest,
    AnalyzeTokenResponse,
    PortfolioInsight,
)


def analyze_portfolio(payload: AnalyzePortfolioRequest) -> AnalyzePortfolioResponse:
    return AnalyzePortfolioResponse(
        address=payload.address,
        chain_id=payload.chain_id,
        overall_summary="Mock analysis: portfolio is diversified across stable and blue-chip assets.",
        insights=[
            PortfolioInsight(
                category="diversification",
                summary="Exposure is spread across ETH, USDC, and VALT sample holdings.",
                severity="low",
            ),
            PortfolioInsight(
                category="risk",
                summary="No transaction, custody, or paid-provider action is performed by this mock.",
                severity="info",
            ),
        ],
    )


def analyze_token(payload: AnalyzeTokenRequest) -> AnalyzeTokenResponse:
    symbol = payload.symbol or "MOCK"
    return AnalyzeTokenResponse(
        token_address=payload.token_address,
        chain_id=payload.chain_id,
        symbol=symbol,
        summary=f"Mock analysis: {symbol} has placeholder metadata and no live market signal.",
        risk_level="medium",
    )
