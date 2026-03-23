"""
NEWSRADAR Backend - FastAPI Application
Proyecto académico - Grado en Ingeniería Informática, UC3M

Sistema de procesamiento y análisis de canales RSS con clasificación automática
mediante IPTC Media Topics y visualización en tiempo real.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from core.config import settings
from db.database import connect_db, disconnect_db, ping_database

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado global de la BD (accesible desde el health check)
_db_connected: bool = False


# ============================================
# Lifespan Events
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionar eventos de inicio y cierre de la aplicación."""
    global _db_connected

    # Startup
    logger.info("Iniciando NEWSRADAR Backend...")
    try:
        await connect_db()
        _db_connected = True
        logger.info("✓ MongoDB conectado — base de datos: %s", settings.DATABASE_NAME)

        # Seed de usuarios iniciales si la BD está vacía
        await _seed_initial_users()

    except Exception as exc:
        _db_connected = False
        logger.warning("⚠  No se pudo conectar a MongoDB: %s", exc)
        logger.warning("   El backend iniciará en modo degradado (sin base de datos)")

    yield

    # Shutdown
    logger.info("Finalizando NEWSRADAR Backend...")
    await disconnect_db()
    _db_connected = False


async def _seed_initial_users() -> None:
    """
    Inserta usuarios semilla (admin + reader) si no existen aún.
    Usa passlib/bcrypt para el hash de contraseñas.
    """
    try:
        from db.database import users_collection
        from passlib.context import CryptContext

        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        col = users_collection()

        seed_users = [
            {
                "email": "admin@newsradar.com",
                "password": "admin123",
                "name": "Admin Manager",
                "role": "gestor_newsradar",
            },
            {
                "email": "reader@newsradar.com",
                "password": "reader123",
                "name": "Reader User",
                "role": "lector",
            },
        ]

        from datetime import datetime

        created = 0
        for u in seed_users:
            exists = await col.find_one({"email": u["email"]})
            if not exists:
                await col.insert_one(
                    {
                        "email": u["email"],
                        "password": pwd_ctx.hash(u["password"]),
                        "name": u["name"],
                        "role": u["role"],
                        "active": True,
                        "preferences": {
                            "iptcSubscriptions": [],
                            "sourceSubscriptions": [],
                            "alertsEnabled": True,
                            "emailNotifications": True,
                            "language": "es",
                        },
                        "createdAt": datetime.utcnow(),
                        "lastLogin": None,
                    }
                )
                created += 1

        if created:
            logger.info("✓ %d usuario(s) semilla creado(s)", created)
        else:
            logger.info("  Usuarios semilla ya existen, omitiendo")

    except Exception as exc:
        logger.warning("  No se pudo crear usuarios semilla: %s", exc)


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
    - Autenticación y autorización (manager / reader)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
    Retorna el estado actual del servicio y la conectividad a la base de datos.
    """
    db_status = "disconnected"
    if _db_connected:
        try:
            await ping_database()
            db_status = "connected"
        except Exception:
            db_status = "error"

    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "NEWSRADAR API",
            "version": "1.0.0",
            "database": {
                "status": db_status,
                "type": "MongoDB",
                "name": settings.DATABASE_NAME,
            },
        },
    )


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Endpoint raíz - Información general de la API."""
    return {
        "message": "Bienvenido a NEWSRADAR API",
        "docs": "/docs",
        "version": "1.0.0",
    }


# ============================================
# Placeholder Endpoints (completar en sprints siguientes)
# ============================================
@app.get("/api/v1/articles", tags=["Articles"])
async def get_articles():
    """Obtener artículos con filtros opcionales."""
    return {"articles": [], "count": 0}


@app.get("/api/v1/sources", tags=["Sources"])
async def get_sources():
    """Obtener lista de fuentes RSS configuradas."""
    return {"sources": [], "count": 0}


@app.get("/api/v1/topics", tags=["Topics"])
async def get_topics():
    """Obtener lista de IPTC Media Topics disponibles."""
    return {"topics": [], "count": 0}


# ============================================
# Custom OpenAPI Schema
# ============================================
def custom_openapi():
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
    logger.error("Error no controlado: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor", "status": "error"},
    )


# ============================================
# Entry point
# ============================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
