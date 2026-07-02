from datetime import UTC, datetime

from app.schemas.portfolio import PortfolioAsset, PortfolioResponse


def get_mock_portfolio(address: str) -> PortfolioResponse:
    assets = [
        PortfolioAsset(
            chain_id=1,
            token_address="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            symbol="ETH",
            name="Ether",
            balance="1.2500",
            value_usd=4375.0,
            allocation_percent=71.43,
            risk_flags=[],
        ),
        PortfolioAsset(
            chain_id=1,
            token_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            symbol="USDC",
            name="USD Coin",
            balance="1250.00",
            value_usd=1250.0,
            allocation_percent=20.41,
            risk_flags=["stablecoin_depeg_risk"],
        ),
        PortfolioAsset(
            chain_id=1,
            token_address="0x0000000000000000000000000000000000000000",
            symbol="VALT",
            name="Valthera Mock Token",
            balance="5000.00",
            value_usd=500.0,
            allocation_percent=8.16,
            risk_flags=["mock_asset", "low_liquidity"],
        ),
    ]

    return PortfolioResponse(
        wallet_address=address,
        chain_id=1,
        total_value_usd=sum(asset.value_usd for asset in assets),
        assets=assets,
        allocation_percent=100.0,
        risk_flags=["mock_data"],
        updated_at=datetime.now(UTC),
    )
