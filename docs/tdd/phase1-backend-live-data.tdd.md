# TDD Evidence Report: Phase 1 — Backend Live Data

## User Journeys
1. User gets real 0x quote — sees actual swap price from DEX aggregator
2. System falls back when 0x fails — still returns quote via next provider
3. User sees real on-chain portfolio — informed trading decisions

## Task Report

### Real 0x API Quote Provider
- Rewrote `app/providers/zerox.py` — real 0x Swap API v1 integration with API key auth
- Test: `pytest tests/test_zerox_provider.py` — 7/7 GREEN
- Guarantees: can_quote for supported chains (1,10,137,42161,8453), rejects unsupported, returns typed ProviderQuote on success, raises on API/network errors, includes API key header

### Real 1inch API Quote Provider
- Rewrote `app/providers/oneinch.py` — real 1inch Swap API v5.2 integration
- Test: `pytest tests/test_oneinch_provider.py` — 6/6 GREEN
- Guarantees: can_quote for supported chains, rejects unsupported, returns ProviderQuote, raises on errors, validates API key

### Real Portfolio via RPC (web3.py)
- Rewrote `app/services/portfolio_service.py` — on-chain ETH balance + ERC-20 token balances via web3.py
- Test: `pytest tests/test_portfolio_rpc.py` — 5/5 GREEN
- Guarantees: validates eth address, returns PortfolioResponse with is_mock=False, handles RPC failure gracefully
- Updated portfolio API endpoint to use real implementation with error handling

### AI Engine — Ollama Integration
- Created `app/services/llm_client.py` — Ollama API client with JSON mode
- Rewrote `app/services/analysis.py` — LLM-first analysis with fallback to rule-based when Ollama unavailable
- Test: `python -m pytest` — 7/7 GREEN
- Guarantees: LLM analysis when Ollama available, graceful fallback with deterministic scoring when unavailable

## Test Specification

| # | What is guaranteed | Test file | Type | Result |
|---|--------------------|-----------|------|--------|
| 1 | 0x can_quote returns True for supported chains | test_zerox_provider:test_can_quote_supported_chain | unit | PASS |
| 2 | 0x can_quote returns False for unsupported chains | test_zerox_provider:test_cannot_quote_unsupported_chain | unit | PASS |
| 3 | 0x get_quote returns ProviderQuote on success | test_zerox_provider:test_get_quote_returns_provider_quote_on_success | unit | PASS |
| 4 | 0x get_quote raises on API error | test_zerox_provider:test_get_quote_raises_on_api_error | unit | PASS |
| 5 | 0x get_quote raises on network error | test_zerox_provider:test_get_quote_raises_on_network_error | unit | PASS |
| 6 | 0x get_quote includes API key header | test_zerox_provider:test_get_quote_includes_api_key_header | unit | PASS |
| 7 | 0x get_quote raises when no API key | test_zerox_provider:test_get_quote_raises_when_no_api_key_configured | unit | PASS |
| 8 | 1inch can_quote for supported chains | test_oneinch_provider:test_can_quote_supported_chain | unit | PASS |
| 9 | 1inch cannot_quote for unsupported chains | test_oneinch_provider:test_cannot_quote_unsupported_chain | unit | PASS |
| 10 | 1inch get_quote returns ProviderQuote | test_oneinch_provider:test_get_quote_returns_provider_quote_on_success | unit | PASS |
| 11 | 1inch get_quote raises on API error | test_oneinch_provider:test_get_quote_raises_on_api_error | unit | PASS |
| 12 | 1inch get_quote raises on network error | test_oneinch_provider:test_get_quote_raises_on_network_error | unit | PASS |
| 13 | 1inch get_quote raises when no API key | test_oneinch_provider:test_get_quote_raises_when_no_api_key | unit | PASS |
| 14 | Portfolio validates invalid eth address | test_portfolio_rpc:test_validate_address_rejects_invalid | unit | PASS |
| 15 | Portfolio validates empty address | test_portfolio_rpc:test_validate_address_rejects_empty | unit | PASS |
| 16 | Portfolio accepts valid address | test_portfolio_rpc:test_validate_address_accepts_valid | unit | PASS |
| 17 | Portfolio returns PortfolioResponse via RPC | test_portfolio_rpc:test_get_portfolio_uses_provided_rpc | unit | PASS |
| 18 | Portfolio handles RPC failure | test_portfolio_rpc:test_get_portfolio_handles_rpc_failure | unit | PASS |
| 19 | Portfolio endpoint returns typed payload | test_portfolio:test_get_portfolio_returns_typed_payload | integration | PASS |
| 20 | Portfolio endpoint rejects invalid address | test_portfolio:test_get_portfolio_rejects_invalid_evm_address | integration | PASS |
| 21 | AI engine portfolio analysis uses LLM | test_analysis:test_portfolio_analysis_uses_llm | unit | PASS |
| 22 | AI engine falls back when LLM unavailable | test_analysis:test_portfolio_analysis_falls_back_when_llm_unavailable | unit | PASS |
| 23 | AI engine token analysis uses LLM | test_analysis:test_token_analysis_uses_llm | unit | PASS |
| 24 | AI engine token fallback when LLM unavailable | test_analysis:test_token_analysis_fallback_when_llm_unavailable | unit | PASS |

## Coverage and Known Gaps
- Quote providers need real API keys (ZEROX_API_KEY, ONEINCH_API_KEY) for live data
- Portfolio RPC needs working WEB3_RPC_URL_1 (defaults to Alchemy demo key)
- AI engine needs Ollama running on localhost:11434 for LLM-powered analysis
- No coverage for 0x/1inch rate limiting or pagination
- Web-app still uses mock data for UI (Phase 2 target)
