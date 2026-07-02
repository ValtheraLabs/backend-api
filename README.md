# Valthera Backend API

The backend API is the coordination layer for portfolio aggregation, market data, AI routing, indexing, jobs, and secure server-side integrations.

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
