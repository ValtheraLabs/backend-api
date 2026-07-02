# Backend API Architecture

## Role

The backend API is the server-side coordination layer for Valthera. It should aggregate data, protect secrets, provide stable APIs, and route AI requests.

## Core Modules

```text
backend-api
├── API Gateway
├── Portfolio Service
├── Token Metadata Service
├── Market Data Service
├── Wallet Activity Service
├── AI Gateway
├── Jobs / Workers
├── Cache Layer
└── Database Layer
```

## MVP Endpoints

```text
GET /health
GET /v1/portfolio/{address}
GET /v1/tokens/{chainId}/{address}
GET /v1/market/summary
POST /v1/ai/analyze-portfolio
POST /v1/ai/analyze-token
```

## Data Flow

1. Web app sends wallet address and chain context.
2. Backend validates request and rate limits.
3. Backend aggregates token balances, token metadata, prices, and activity.
4. Backend optionally sends structured context to ai-engine.
5. Backend returns typed JSON responses to web-app.

## Security Requirements

- Never store private keys.
- Keep API keys server-side only.
- Rate limit public endpoints.
- Validate wallet addresses, chain IDs, and token addresses.
- Log errors without leaking secrets.
- Prefer typed DTOs and schema validation.

## First Implementation Target

A minimal API service with health check, OpenAPI docs, Docker setup, portfolio stub, and AI gateway stub.
