from app.schemas.ai import (
    AnalyzePortfolioRequest,
    AnalyzePortfolioResponse,
    AnalyzeTokenRequest,
    AnalyzeTokenResponse,
    PortfolioInsight,
)
from app.services.ai_client import (
    AIEngineClient,
    PortfolioAnalysisPayload,
    TokenAnalysisPayload,
)


def analyze_portfolio(payload: AnalyzePortfolioRequest) -> AnalyzePortfolioResponse:
    ai_response = AIEngineClient().analyze_portfolio(
        PortfolioAnalysisPayload(
            wallet_address=payload.address,
            chain_id=payload.chain_id,
            assets=[],
            include_recommendations=True,
        )
    )

    return AnalyzePortfolioResponse(
        address=payload.address,
        chain_id=payload.chain_id,
        overall_summary=ai_response.summary,
        insights=[
            PortfolioInsight(
                category=factor.name,
                summary=factor.explanation,
                severity=factor.severity,
            )
            for factor in ai_response.risk_factors
        ],
        analysis_id=ai_response.analysis_id,
        risk_score=ai_response.risk_score,
        confidence=ai_response.confidence,
        risk_factors=ai_response.risk_factors,
        recommended_actions=ai_response.recommended_actions,
        disclaimer=ai_response.disclaimer,
        is_mock=True,
        source="ai-engine",
    )


def analyze_token(payload: AnalyzeTokenRequest) -> AnalyzeTokenResponse:
    symbol = payload.symbol or "MOCK"
    ai_response = AIEngineClient().analyze_token(
        TokenAnalysisPayload(
            token_address=payload.token_address,
            chain_id=payload.chain_id,
            symbol=symbol,
            include_contract_signals=True,
        )
    )

    return AnalyzeTokenResponse(
        token_address=payload.token_address,
        chain_id=payload.chain_id,
        symbol=ai_response.token_symbol,
        summary=ai_response.summary,
        risk_level=ai_response.confidence,
        analysis_id=ai_response.analysis_id,
        risk_score=ai_response.risk_score,
        confidence=ai_response.confidence,
        risk_factors=ai_response.risk_factors,
        recommended_actions=ai_response.recommended_actions,
        disclaimer=ai_response.disclaimer,
        is_mock=True,
        source="ai-engine",
    )
