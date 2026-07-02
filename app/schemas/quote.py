from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class QuoteRouteStep(BaseModel):
    label: str
    provider: str
    token_in: str
    token_out: str


class QuoteResponse(BaseModel):
    chain_id: int = Field(..., ge=1)
    token_in: str
    token_out: str
    amount_in: Decimal = Field(..., gt=0)
    amount_out_estimate: Decimal = Field(..., ge=0)
    price_impact_percent: Decimal = Field(..., ge=0)
    slippage_bps: int = Field(..., ge=0)
    route: list[QuoteRouteStep]
    gas_estimate: int = Field(..., ge=0)
    provider: str
    warnings: list[str]
    updated_at: datetime
    is_mock: bool = True
