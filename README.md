# Valthera Backend API

The backend API is the coordination layer for portfolio aggregation, market data, AI routing, indexing, jobs, and secure server-side integrations.

## MVP-003 FastAPI Skeleton

This milestone provides a runnable Python 3.12+ FastAPI backend with typed Pydantic schemas, mock portfolio data, AI analysis endpoints backed by the local `ai-engine` service, and no real provider keys.

The quote endpoint returns typed mock swap quotes only. It does not perform real DEX routing, build transactions, sign transactions, or use paid provider keys.

## Requirements

- Python 3.12+
- pip

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

The API will be available at `http://127.0.0.1:8000`.

Backend AI routes call `ai-engine`. Run `ai-engine` separately on port `8001`:

```bash
uvicorn app.main:app --reload --port 8001
```

Then set:

```bash
AI_ENGINE_BASE_URL=http://localhost:8001
```

If `ai-engine` is unavailable or times out, the backend returns `503` with a typed JSON error:

```json
{
  "error": "ai_engine_unavailable",
  "message": "AI engine is unavailable.",
  "ai_engine_base_url": "http://localhost:8001"
}
```

## Endpoints

- `GET /health`
- `GET /v1/portfolio/{address}`
- `GET /v1/quote`
- `POST /v1/ai/analyze-portfolio`
- `POST /v1/ai/analyze-token`

Interactive OpenAPI docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Example Requests

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/portfolio/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

```bash
curl "http://127.0.0.1:8000/v1/quote?chain_id=1&token_in=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&token_out=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount_in=1.5&slippage_bps=50"
```

```bash
curl -X POST http://127.0.0.1:8000/v1/ai/analyze-portfolio \
  -H "Content-Type: application/json" \
  -d "{\"address\":\"0x123\",\"chain_id\":1}"
```

```bash
curl -X POST http://127.0.0.1:8000/v1/ai/analyze-token \
  -H "Content-Type: application/json" \
  -d "{\"token_address\":\"0xabc\",\"chain_id\":1,\"symbol\":\"VALT\"}"
```

## Configuration

Copy `.env.example` to `.env` for local overrides. Do not commit real secrets, private keys, or paid provider credentials.

Useful local values:

```bash
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
AI_ENGINE_BASE_URL=http://localhost:8001
AI_ENGINE_TIMEOUT_SECONDS=5
```

No LLM keys, private keys, or transaction execution credentials are required for local development.

## Portfolio Response Shape

`GET /v1/portfolio/{address}` validates that `address` is an EVM wallet address in `0x` plus 40 hexadecimal characters format.

```json
{
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "chain_id": 1,
  "total_value_usd": 6125.0,
  "assets": [
    {
      "chain_id": 1,
      "token_address": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
      "symbol": "ETH",
      "name": "Ether",
      "balance": "1.2500",
      "value_usd": 4375.0,
      "allocation_percent": 71.43,
      "risk_flags": []
    }
  ],
  "allocation_percent": 100.0,
  "risk_flags": ["mock_data"],
  "updated_at": "2026-07-02T20:00:00Z",
  "is_mock": true
}
```

## Quote Response Shape

`GET /v1/quote` validates `token_in` and `token_out` as EVM token addresses and requires `amount_in > 0`.

```json
{
  "chain_id": 1,
  "token_in": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
  "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "amount_in": "1.5",
  "amount_out_estimate": "2700.000000",
  "price_impact_percent": "0.12",
  "slippage_bps": 50,
  "route": [
    {
      "label": "Mock direct route",
      "provider": "valthera-mock-quote-engine",
      "token_in": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
      "token_out": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    }
  ],
  "gas_estimate": 150000,
  "provider": "valthera-mock-quote-engine",
  "warnings": ["Mock quote only. No DEX routing has been performed."],
  "updated_at": "2026-07-02T20:00:00Z",
  "is_mock": true
}
```

## Purpose

Provide trusted backend services for the Valthera web app, AI engine, and future developer APIs.

## MVP Responsibilities

- Portfolio aggregation
- Token metadata aggregation
- Market data gateway
- Mock quote engine
- AI engine gateway via `AI_ENGINE_BASE_URL`
- Wallet activity indexing
- API rate limiting
- Background jobs
- Structured API responses

## Preferred Stack

- FastAPI or Node.js/NestJS
- PostgreSQL
- Redis
- Docker
- OpenAPI
- Background workers

## Security Rule

The backend must never hold user private keys. It may prepare data, simulate actions, and aggregate information, but user transactions must be signed client-side by the user's wallet.

## First Milestone

Build a health-check API, OpenAPI schema, portfolio endpoint stub, token metadata endpoint stub, and AI gateway endpoint stub.
