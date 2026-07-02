from typing import Any, cast

import httpx
from pydantic import BaseModel, Field, ValidationError

from app.core.config import settings
from app.schemas.ai import RecommendedAction, RiskFactor


class AIEngineUnavailableError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PortfolioAssetPayload(BaseModel):
    symbol: str
    allocation_percent: float = Field(..., ge=0, le=100)
    estimated_value_usd: float | None = Field(default=None, ge=0)


class PortfolioAnalysisPayload(BaseModel):
    wallet_address: str | None = None
    chain_id: int | None = Field(default=None, ge=1)
    assets: list[PortfolioAssetPayload] = Field(default_factory=list)
    include_recommendations: bool = True


class PortfolioAnalysisResult(BaseModel):
    analysis_id: str
    summary: str
    risk_score: int = Field(..., ge=0, le=100)
    confidence: str
    risk_factors: list[RiskFactor]
    recommended_actions: list[RecommendedAction]
    disclaimer: str


class TokenAnalysisPayload(BaseModel):
    token_address: str | None = None
    symbol: str | None = None
    chain_id: int | None = Field(default=None, ge=1)
    include_contract_signals: bool = True


class TokenAnalysisResult(BaseModel):
    analysis_id: str
    token_symbol: str
    summary: str
    risk_score: int = Field(..., ge=0, le=100)
    confidence: str
    risk_factors: list[RiskFactor]
    recommended_actions: list[RecommendedAction]
    disclaimer: str


def _create_http_client() -> httpx.Client:
    return httpx.Client(
        base_url=settings.ai_engine_base_url,
        timeout=settings.ai_engine_timeout_seconds,
    )


class AIEngineClient:
    def analyze_portfolio(
        self,
        payload: PortfolioAnalysisPayload,
    ) -> PortfolioAnalysisResult:
        data = self._post("/v1/analyze/portfolio", payload)
        try:
            return PortfolioAnalysisResult.model_validate(data)
        except ValidationError as exc:
            raise AIEngineUnavailableError(
                "AI engine returned an invalid response."
            ) from exc

    def analyze_token(self, payload: TokenAnalysisPayload) -> TokenAnalysisResult:
        data = self._post("/v1/analyze/token", payload)
        try:
            return TokenAnalysisResult.model_validate(data)
        except ValidationError as exc:
            raise AIEngineUnavailableError(
                "AI engine returned an invalid response."
            ) from exc

    def _post(self, path: str, payload: BaseModel) -> dict[str, Any]:
        try:
            with _create_http_client() as client:
                response = client.post(
                    path,
                    json=payload.model_dump(exclude_none=True),
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
        except ValueError as exc:
            raise AIEngineUnavailableError(
                "AI engine returned an invalid response."
            ) from exc
        except httpx.TimeoutException as exc:
            raise AIEngineUnavailableError("AI engine request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise AIEngineUnavailableError(
                "AI engine returned an unsuccessful response.",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise AIEngineUnavailableError("AI engine is unavailable.") from exc
