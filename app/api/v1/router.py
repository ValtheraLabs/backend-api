from fastapi import APIRouter

from app.api.quote import router as quote_router
from app.api.v1.ai import router as ai_router
from app.api.v1.portfolio import router as portfolio_router

router = APIRouter()
router.include_router(portfolio_router)
router.include_router(ai_router)
router.include_router(quote_router)
