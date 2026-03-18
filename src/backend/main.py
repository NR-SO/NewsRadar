"""
NEWSRADAR Backend - FastAPI Application
Proyecto académico - Grado en Ingeniería Informática, UC3M

Sistema de procesamiento y análisis de canales RSS con clasificación automática
mediante IPTC Media Topics y visualización en tiempo real.
"""

import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================
# Lifespan Events
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionar eventos de inicio y cierre de la aplicación.
    """
    # Startup
    logger.info("🚀 NEWSRADAR Backend iniciando...")
    logger.info("✓ Conexión a base de datos establecida")
    logger.info("✓ Configuración cargada exitosamente")
    
    yield
    
    # Shutdown
    logger.info("🛑 NEWSRADAR Backend finalizando...")
    logger.info("✓ Recursos liberados")


# ============================================
# Crear aplicación FastAPI
# ============================================
app = FastAPI(
    title="NEWSRADAR API",
    description="""
    API REST para procesamiento y análisis de canales RSS.
    
    - Agregación de múltiples fuentes RSS
    - Clasificación automática con IPTC Media Topics
    - Visualización interactiva en tiempo real
    - Autenticación y autorización
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# ============================================
# Middleware - CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Health Check Endpoints
# ============================================
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Endpoint de verificación de salud de la API.
    Retorna el estado actual del servicio.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "NEWSRADAR API",
            "version": "1.0.0"
        }
    )


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """
    Endpoint raíz - Información general de la API.
    """
    return {
        "message": "Bienvenido a NEWSRADAR API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# ============================================
# Placeholder Endpoints (completar en sprint 2)
# ============================================
@app.get("/api/v1/articles", tags=["Articles"])
async def get_articles():
    """
    Obtener artículos con filtros opcionales.
    """
    return {"articles": [], "count": 0}


@app.get("/api/v1/sources", tags=["Sources"])
async def get_sources():
    """
    Obtener lista de fuentes RSS configuradas.
    """
    return {"sources": [], "count": 0}


@app.get("/api/v1/topics", tags=["Topics"])
async def get_topics():
    """
    Obtener lista de IPTC Media Topics disponibles.
    """
    return {"topics": [], "count": 0}


# ============================================
# Custom OpenAPI Schema
# ============================================
def custom_openapi():
    """
    Personalizar esquema OpenAPI.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="NEWSRADAR API",
        version="1.0.0",
        description="API REST para procesamiento de canales RSS",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ============================================
# Error Handlers
# ============================================
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Manejar excepciones generales
    """
    logger.error(f"Error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "status": "error"
        }
    )


# ============================================
# Entry point
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
