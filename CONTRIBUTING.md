# Contributing to Valthera Backend API

## Development Rules

- Use typed request and response schemas.
- Validate all external input.
- Keep secrets out of source control.
- Keep blockchain provider keys server-side.
- Prefer explicit errors over silent failures.
- Add tests for service logic.

## PR Requirements

Every backend PR should include:

- What changed
- API endpoints affected
- How to test locally
- Database/cache changes if any
- Security considerations

## Security Requirements

- No private keys.
- No hardcoded API credentials.
- No unbounded public endpoints.
- No AI endpoint that can trigger transactions directly.
- No unauthenticated admin functionality.
