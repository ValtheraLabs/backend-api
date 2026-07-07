from datetime import UTC, datetime
from decimal import Decimal

from web3 import Web3

from app.core.config import settings
from app.schemas.portfolio import PortfolioAsset, PortfolioResponse

ERC20_BALANCE_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

ETH_PRICE_USD = 3500.0

COMMON_TOKENS: dict[str, dict[str, object]] = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "price_usd": 1.0,
    },
    "0xdac17f958d2ee523a2206206994597c13d831ec7": {
        "symbol": "USDT",
        "name": "Tether USD",
        "decimals": 6,
        "price_usd": 1.0,
    },
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {
        "symbol": "WBTC",
        "name": "Wrapped Bitcoin",
        "decimals": 8,
        "price_usd": 65000.0,
    },
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
        "symbol": "WETH",
        "name": "Wrapped Ether",
        "decimals": 18,
        "price_usd": ETH_PRICE_USD,
    },
}


def _validate_address(address: str) -> None:
    if not address or not Web3.is_address(address):
        raise ValueError(f"Invalid Ethereum address: {address}")


def _get_eth_balance(w3: Web3, address: str) -> PortfolioAsset:
    balance_wei = w3.eth.get_balance(address)
    balance_eth = float(Web3.from_wei(balance_wei, "ether"))
    value_usd = round(balance_eth * ETH_PRICE_USD, 2)

    return PortfolioAsset(
        chain_id=1,
        token_address="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        symbol="ETH",
        name="Ether",
        balance=f"{balance_eth:.4f}",
        value_usd=value_usd,
        allocation_percent=0,
        risk_flags=[],
    )


def _get_token_balance(
    w3: Web3, address: str, token_address: str, token_info: dict[str, object]
) -> PortfolioAsset | None:
    try:
        checksummed = Web3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=checksummed, abi=ERC20_BALANCE_ABI)
        balance_raw = contract.functions.balanceOf(address).call()
        decimals = token_info.get("decimals", 18)
        balance = balance_raw / (10 ** int(decimals))
        price_usd = float(token_info.get("price_usd", 0))
        value_usd = round(balance * price_usd, 2)

        if value_usd < 0.01:
            return None

        return PortfolioAsset(
            chain_id=1,
            token_address=token_address,
            symbol=str(token_info["symbol"]),
            name=str(token_info["name"]),
            balance=f"{balance:.4f}",
            value_usd=value_usd,
            allocation_percent=0,
            risk_flags=[],
        )
    except Exception:
        return None


def get_portfolio(
    address: str,
    rpc_url: str | None = None,
) -> PortfolioResponse:
    _validate_address(address)

    url = rpc_url or settings.web3_rpc_url_1
    w3 = Web3(Web3.HTTPProvider(url))

    if not w3.is_connected():
        raise RuntimeError(
            "Unable to connect to RPC endpoint. Check WEB3_RPC_URL_1."
        )

    assets: list[PortfolioAsset] = []

    eth = _get_eth_balance(w3, address)
    assets.append(eth)

    for token_address, token_info in COMMON_TOKENS.items():
        token = _get_token_balance(w3, address, str(token_address), token_info)
        if token is not None:
            assets.append(token)

    total_value = sum(a.value_usd for a in assets)
    for asset in assets:
        if total_value > 0:
            asset.allocation_percent = round((asset.value_usd / total_value) * 100, 2)

    risk_flags: list[str] = []
    if eth.value_usd > 0 and (eth.value_usd / total_value) > 0.8:
        risk_flags.append("high_eth_concentration")

    return PortfolioResponse(
        wallet_address=address,
        chain_id=1,
        total_value_usd=round(total_value, 2),
        assets=assets,
        allocation_percent=100.0,
        risk_flags=risk_flags,
        updated_at=datetime.now(UTC),
        is_mock=False,
    )
