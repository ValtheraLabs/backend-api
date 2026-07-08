from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class QuoteResponse(BaseModel):
    provider: str = Field(..., examples=["uniswap-v3-quoter"])
    chain_id: int = Field(..., ge=1, examples=[1])
    token_in: str = Field(..., examples=["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"])
    token_out: str = Field(..., examples=["0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"])
    amount_in: Decimal = Field(..., gt=0, examples=["1.5"])
    amount_out: Decimal = Field(..., ge=0, examples=["2700.000000"])
    estimated_gas: int = Field(..., ge=0, examples=[150000])
    price_impact: Decimal = Field(..., ge=0, examples=["0.12"])
    slippage_bps: int = Field(..., ge=0, examples=[50])
    route: list[str] = Field(..., examples=[["Uniswap V3 Quoter", "Mock pool path"]])
    timestamp: datetime
    warnings: list[str]
    is_mock: bool = True
    to: str = ""
    data: str = ""
    value: str = "0"
