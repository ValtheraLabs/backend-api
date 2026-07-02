# Quote Providers

## Interface

Quote providers implement `QuoteProvider` from `app/providers/base.py`.

Each provider exposes:

- `name`
- `can_quote(request)`
- `get_quote(request)`

## Registry

`app/providers/registry.py` defines provider priority:

1. Uniswap V3 Quoter
2. 0x API
3. 1inch

## Fallback

`QuoteProviderService` tries providers in order. If a provider fails, the service records a warning and tries the next eligible provider.

## Current Live Status

The Uniswap provider is the first provider adapter and returns a quote-only response without transaction construction. 0x and 1inch are registered fallback providers, but they fail closed until API credentials and network integration are explicitly configured.

No paid provider keys, private keys, signing, or transaction submission are included.
