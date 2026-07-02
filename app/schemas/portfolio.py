from datetime import datetime

from pydantic import BaseModel, Field


class PortfolioAsset(BaseModel):
    chain_id: int
    token_address: str
    symbol: str
    name: str
    balance: str
    value_usd: float = Field(..., ge=0)
    allocation_percent: float = Field(..., ge=0, le=100)
    risk_flags: list[str]


class PortfolioResponse(BaseModel):
    wallet_address: str
    chain_id: int
    total_value_usd: float = Field(..., ge=0)
    assets: list[PortfolioAsset]
    allocation_percent: float = Field(..., ge=0, le=100)
    risk_flags: list[str]
    updated_at: datetime
    is_mock: bool = True
