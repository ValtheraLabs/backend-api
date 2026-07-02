# API

Base path:

```text
/api/v1
```

## Health

```http
GET /api/v1/health
```

Response:

```json
{
  "status": "ok",
  "service": "backend-api"
}
```

## Quote

```http
GET /api/v1/quote
```

Query params:

- `chain_id`
- `token_in`
- `token_out`
- `amount_in`
- `slippage_bps`

Example:

```bash
curl "http://localhost:8000/api/v1/quote?chain_id=1&token_in=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&token_out=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amount_in=1.5&slippage_bps=50"
```

The endpoint validates EVM token addresses and requires `amount_in > 0`.

## AI

```http
POST /api/v1/ai/analyze-portfolio
POST /api/v1/ai/analyze-token
```

AI requests are routed through `backend-api` to `ai-engine`.
