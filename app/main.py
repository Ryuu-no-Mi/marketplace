"""Main application module - Hexagonal Architecture."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.database import engine, Base
from app.presentation.api import api_router

# Create FastAPI application
app = FastAPI(
    title="Marketplace API",
    description="A modern marketplace API built with Hexagonal Architecture",
    version="1.0.0",
)

# Include API routers
app.include_router(api_router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Marketplace API is running",
        "version": "1.0.0"
    }


@app.on_event("startup")
async def startup():
    """Startup event."""
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

