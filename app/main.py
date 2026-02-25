"""
Punto de entrada principal de la aplicación FastAPI.
Responsabilidades:
- Crea la aplicación FastAPI
- Configuran los routers
- Configuran CORS, eventos, middleware, etc.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import product_router, user_router
from app.core.database import engine
from app.infrastructure.repositories.models import Base


# Crear las tablas al iniciar (solo si no existen)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Evento de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar.
    """
    # Startup: Crear tablas
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada")
    
    yield  # La app corre aquí
    
    # Shutdown: Limpiar recursos
    print("Cerrando aplicación...")


# Crear instancia de FastAPI
app = FastAPI(
    title="Marketplace API",
    description="API de marketplace con arquitectura hexagonal",
    version="1.0.0",
    lifespan=lifespan
)


# CORS: Configurar orígenes permitidos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["https://app.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(product_router, prefix="/api")
app.include_router(user_router, prefix="/api")


# Health check
@app.get("/", tags=["Health"])
def health_check():
    """Endpoint de salud de la aplicación."""
    return {
        "status": "healthy",
        "service": "Marketplace API",
        "version": "1.0.0"
    }


# Punto de entrada
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
