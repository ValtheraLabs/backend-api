# Valthera Backend API

Production-ready FastAPI backend for Valthera infrastructure, AI routing, portfolio data, and quote provider orchestration.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docker:

```bash
docker compose up
```

## Configuration

Copy `.env.example` to `.env`.

Key settings:

- `APP_ENV`
- `APP_NAME`
- `APP_VERSION`
- `HOST`
- `PORT`
- `AI_ENGINE_BASE_URL`
- `REDIS_URL`
- `DATABASE_URL`
- `LOG_LEVEL`
- `QUOTE_CACHE_TTL`
- `CORS_ORIGINS`

## API

Primary API prefix:

```text
/api/v1
```

Endpoints:

- `GET /api/v1/health`
- `GET /api/v1/portfolio/{address}`
- `GET /api/v1/quote`
- `POST /api/v1/ai/analyze-portfolio`
- `POST /api/v1/ai/analyze-token`

Temporary MVP compatibility paths remain available under `/v1`.

## Quote Example

```bash
curl "http://localhost:8000/api/v1/quote?chain_id=1&token_in=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&token_out=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount_in=1.5&slippage_bps=50"
```

The quote layer uses a provider abstraction with priority:

1. Uniswap V3 Quoter
2. 0x API
3. 1inch

Provider fallback and TTL quote caching are implemented. The current provider adapters are quote-only and do not build or submit transactions.

## Tooling

```bash
make test
make lint
make typecheck
make check
```

Pre-commit:

```bash
pre-commit install
pre-commit run --all-files
```

## Security

No private keys, paid provider keys, transaction signing, transaction building, or transaction submission are included. Rate limiting and input validation are enabled.

## Documentation

- `docs/Architecture.md`
- `docs/Providers.md`
- `docs/API.md`
