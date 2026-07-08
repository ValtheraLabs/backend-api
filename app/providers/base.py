from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class QuoteRequest(BaseModel):
    chain_id: int = Field(..., ge=1)
    token_in: str
    token_out: str
    amount_in: Decimal = Field(..., gt=0)
    slippage_bps: int = Field(..., ge=0)


class ProviderQuote(BaseModel):
    provider: str
    token_in: str
    token_out: str
    amount_in: Decimal = Field(..., gt=0)
    amount_out: Decimal = Field(..., ge=0)
    estimated_gas: int = Field(..., ge=0)
    price_impact: Decimal = Field(..., ge=0)
    route: list[str]
    timestamp: datetime
    warnings: list[str]
    to: str = ""
    data: str = ""
    value: str = "0"


class QuoteProviderError(Exception):
    pass


class QuoteProvider(ABC):
    name: str

    @abstractmethod
    def can_quote(self, request: QuoteRequest) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_quote(self, request: QuoteRequest) -> ProviderQuote:
        raise NotImplementedError
