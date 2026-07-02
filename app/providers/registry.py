from app.providers.base import QuoteProvider
from app.providers.oneinch import OneInchProvider
from app.providers.uniswap import UniswapV3QuoterProvider
from app.providers.zerox import ZeroXProvider


def get_default_providers() -> list[QuoteProvider]:
    return [
        UniswapV3QuoterProvider(),
        ZeroXProvider(),
        OneInchProvider(),
    ]
