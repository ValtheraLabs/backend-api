# Backend Architecture

## Overview

`backend-api` is the server-side gateway for Valthera. It exposes versioned APIs, validates user input, routes AI requests to `ai-engine`, and provides quote responses through a provider abstraction.

## Runtime

- FastAPI application in `app/main.py`
- Versioned API mounted at `/api/v1`
- Temporary MVP compatibility mount at `/v1`
- Pydantic Settings in `app/core/config.py`
- Structured request logging middleware
- In-memory rate limiting middleware
- In-memory TTL cache for quote responses

## Safety

The backend does not store private keys, build transactions, sign transactions, or submit transactions. Quote providers are quote-only and return data for user review.

## Local Entry Points

```bash
uvicorn app.main:app --reload
```

```bash
docker compose up
```
