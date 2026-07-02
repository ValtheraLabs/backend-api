from pydantic import BaseModel


class TokenHolding(BaseModel):
    chain_id: int
    token_address: str
    symbol: str
    name: str
    balance: str
    usd_value: float


class PortfolioResponse(BaseModel):
    address: str
    total_usd_value: float
    holdings: list[TokenHolding]
    is_mock: bool = True
