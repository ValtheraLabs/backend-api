from pydantic import BaseModel, Field


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
    is_mock: bool = True


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
    is_mock: bool = True
