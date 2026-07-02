from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.schemas.ai import (
    AIEngineErrorResponse,
    AnalyzePortfolioRequest,
    AnalyzePortfolioResponse,
    AnalyzeTokenRequest,
    AnalyzeTokenResponse,
)
from app.services.ai_service import analyze_portfolio, analyze_token
from app.services.ai_client import AIEngineUnavailableError

router = APIRouter(prefix="/ai", tags=["ai"])


def _ai_engine_unavailable_response(exc: AIEngineUnavailableError) -> JSONResponse:
    body = AIEngineErrorResponse(
        error="ai_engine_unavailable",
        message=exc.message,
        ai_engine_base_url=settings.ai_engine_base_url,
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body.model_dump(),
    )


@router.post(
    "/analyze-portfolio",
    response_model=AnalyzePortfolioResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": AIEngineErrorResponse}},
)
def analyze_portfolio_endpoint(
    payload: AnalyzePortfolioRequest,
) -> AnalyzePortfolioResponse | JSONResponse:
    try:
        return analyze_portfolio(payload)
    except AIEngineUnavailableError as exc:
        return _ai_engine_unavailable_response(exc)


@router.post(
    "/analyze-token",
    response_model=AnalyzeTokenResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": AIEngineErrorResponse}},
)
def analyze_token_endpoint(
    payload: AnalyzeTokenRequest,
) -> AnalyzeTokenResponse | JSONResponse:
    try:
        return analyze_token(payload)
    except AIEngineUnavailableError as exc:
        return _ai_engine_unavailable_response(exc)
