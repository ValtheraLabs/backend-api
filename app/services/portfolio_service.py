from app.schemas.portfolio import PortfolioResponse, TokenHolding


def get_mock_portfolio(address: str) -> PortfolioResponse:
    holdings = [
        TokenHolding(
            chain_id=1,
            token_address="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            symbol="ETH",
            name="Ether",
            balance="1.2500",
            usd_value=4375.0,
        ),
        TokenHolding(
            chain_id=1,
            token_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            symbol="USDC",
            name="USD Coin",
            balance="1250.00",
            usd_value=1250.0,
        ),
        TokenHolding(
            chain_id=1,
            token_address="0x0000000000000000000000000000000000000000",
            symbol="VALT",
            name="Valthera Mock Token",
            balance="5000.00",
            usd_value=500.0,
        ),
    ]

    return PortfolioResponse(
        address=address,
        total_usd_value=sum(holding.usd_value for holding in holdings),
        holdings=holdings,
    )
