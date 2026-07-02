import httpx

from app.core.config import settings
from app.schemas.ai import (
    AnalyzePortfolioRequest,
    AnalyzePortfolioResponse,
    AnalyzeTokenRequest,
    AnalyzeTokenResponse,
    PortfolioInsight,
)


def _post_ai_engine(path: str, payload: dict) -> dict | None:
    try:
        with httpx.Client(
            base_url=settings.ai_engine_base_url,
            timeout=settings.ai_engine_timeout_seconds,
        ) as client:
            response = client.post(path, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        return None


def analyze_portfolio(payload: AnalyzePortfolioRequest) -> AnalyzePortfolioResponse:
    ai_response = _post_ai_engine(
        "/v1/analyze/portfolio",
        {
            "wallet_address": payload.address,
            "chain_id": payload.chain_id,
            "assets": [],
            "include_recommendations": True,
        },
    )

    if ai_response is not None:
        risk_factors = ai_response.get("risk_factors", [])
        return AnalyzePortfolioResponse(
            address=payload.address,
            chain_id=payload.chain_id,
            overall_summary=ai_response["summary"],
            insights=[
                PortfolioInsight(
                    category=factor["name"],
                    summary=factor["explanation"],
                    severity=factor["severity"],
                )
                for factor in risk_factors
            ],
            analysis_id=ai_response.get("analysis_id"),
            risk_score=ai_response.get("risk_score"),
            confidence=ai_response.get("confidence"),
            risk_factors=risk_factors,
            recommended_actions=ai_response.get("recommended_actions", []),
            disclaimer=ai_response.get("disclaimer"),
            source="ai-engine",
        )

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
        source="backend-fallback",
    )


def analyze_token(payload: AnalyzeTokenRequest) -> AnalyzeTokenResponse:
    symbol = payload.symbol or "MOCK"
    ai_response = _post_ai_engine(
        "/v1/analyze/token",
        {
            "token_address": payload.token_address,
            "chain_id": payload.chain_id,
            "symbol": symbol,
            "include_contract_signals": True,
        },
    )

    if ai_response is not None:
        risk_score = ai_response.get("risk_score")
        return AnalyzeTokenResponse(
            token_address=payload.token_address,
            chain_id=payload.chain_id,
            symbol=ai_response.get("token_symbol", symbol),
            summary=ai_response["summary"],
            risk_level=ai_response.get("confidence", "unknown"),
            analysis_id=ai_response.get("analysis_id"),
            risk_score=risk_score,
            confidence=ai_response.get("confidence"),
            risk_factors=ai_response.get("risk_factors", []),
            recommended_actions=ai_response.get("recommended_actions", []),
            disclaimer=ai_response.get("disclaimer"),
            source="ai-engine",
        )

    return AnalyzeTokenResponse(
        token_address=payload.token_address,
        chain_id=payload.chain_id,
        symbol=symbol,
        summary=f"Mock analysis: {symbol} has placeholder metadata and no live market signal.",
        risk_level="medium",
        source="backend-fallback",
    )
