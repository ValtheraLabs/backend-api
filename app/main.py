from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import RateLimitMiddleware, StructuredLoggingMiddleware

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready backend API for Valthera.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(StructuredLoggingMiddleware)

app.include_router(v1_router, prefix=settings.api_v1_prefix)

# Temporary compatibility while clients migrate from MVP paths to /api/v1.
app.include_router(v1_router, prefix="/v1")
