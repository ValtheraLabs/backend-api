import logging
from time import monotonic
from uuid import uuid4

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from app.core.config import settings

access_logger = logging.getLogger("valthera.access")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        started_at = monotonic()
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            latency = round((monotonic() - started_at) * 1000, 2)
            access_logger.info(
                "request",
                extra={
                    "request_id": request_id,
                    "latency": latency,
                    "status": status_code,
                    "method": request.method,
                    "path": request.url.path,
                },
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._requests: dict[str, list[float]] = {}

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        client_host = request.client.host if request.client else "unknown"
        now = monotonic()
        window_start = now - settings.rate_limit_window_seconds
        request_times = [
            item for item in self._requests.get(client_host, []) if item >= window_start
        ]

        if len(request_times) >= settings.rate_limit_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "rate_limited",
                    "message": "Too many requests.",
                },
            )

        request_times.append(now)
        self._requests[client_host] = request_times
        return await call_next(request)
