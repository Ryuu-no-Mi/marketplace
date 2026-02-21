"""API routes initialization."""

from fastapi import APIRouter
from app.presentation.api.category_routes import router as category_router
from app.presentation.api.product_routes import router as product_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(category_router)
api_router.include_router(product_router)

__all__ = ["api_router"]
