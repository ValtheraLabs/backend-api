from pydantic import BaseModel, Field


class RiskFactor(BaseModel):
    name: str
    severity: str
    explanation: str


class RecommendedAction(BaseModel):
    label: str
    rationale: str
    priority: str


class AnalyzePortfolioRequest(BaseModel):
    address: str = Field(..., min_length=1)
    chain_id: int = Field(default=1, ge=1)
    risk_profile: str | None = Field(default=None, max_length=64)


class PortfolioInsight(BaseModel):
    category: str
    summary: str
    severity: str


class AnalyzePortfolioResponse(BaseModel):
    address: str
    chain_id: int
    overall_summary: str
    insights: list[PortfolioInsight]
    analysis_id: str | None = None
    risk_score: int | None = Field(default=None, ge=0, le=100)
    confidence: str | None = None
    risk_factors: list[RiskFactor] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    disclaimer: str | None = None
    is_mock: bool = True
    source: str = "backend"


class AnalyzeTokenRequest(BaseModel):
    token_address: str = Field(..., min_length=1)
    chain_id: int = Field(default=1, ge=1)
    symbol: str | None = Field(default=None, max_length=32)


class AnalyzeTokenResponse(BaseModel):
    token_address: str
    chain_id: int
    symbol: str | None
    summary: str
    risk_level: str
    analysis_id: str | None = None
    risk_score: int | None = Field(default=None, ge=0, le=100)
    confidence: str | None = None
    risk_factors: list[RiskFactor] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    disclaimer: str | None = None
    is_mock: bool = True
    source: str = "backend"
