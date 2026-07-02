# Valthera Backend API

The backend API is the coordination layer for portfolio aggregation, market data, AI routing, indexing, jobs, and secure server-side integrations.

## MVP-003 FastAPI Skeleton

This milestone provides a runnable Python 3.12+ FastAPI backend with typed Pydantic schemas, mock portfolio data, mock AI analysis endpoints, and no real provider keys.

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

## Endpoints

- `GET /health`
- `GET /v1/portfolio/{address}`
- `POST /v1/ai/analyze-portfolio`
- `POST /v1/ai/analyze-token`

Interactive OpenAPI docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Example Requests

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/portfolio/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
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

## Purpose

Provide trusted backend services for the Valthera web app, AI engine, and future developer APIs.

## MVP Responsibilities

- Portfolio aggregation
- Token metadata aggregation
- Market data gateway
- AI engine gateway
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
