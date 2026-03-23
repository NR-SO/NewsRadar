"""
Capa de conexión a MongoDB para NEWSRADAR.
Gestiona el cliente Motor (async), validación de conexión y acceso a colecciones.
"""
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from core.config import settings

logger = logging.getLogger(__name__)


class _DatabaseState:
    """Singleton que mantiene el cliente y la base de datos activos."""
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


_state = _DatabaseState()


async def connect_db() -> None:
    """Inicializa el cliente Motor y verifica la conexión con un ping."""
    _state.client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        serverSelectionTimeoutMS=5000,  # 5 s de timeout al seleccionar servidor
    )
    _state.db = _state.client[settings.DATABASE_NAME]
    # Verificar la conexión efectivamente
    await ping_database()
    logger.info("✓ Conexión a MongoDB establecida — base de datos: %s", settings.DATABASE_NAME)


async def disconnect_db() -> None:
    """Cierra el cliente Motor de forma limpia."""
    if _state.client is not None:
        _state.client.close()
        _state.client = None
        _state.db = None
        logger.info("✓ Conexión a MongoDB cerrada")


async def ping_database() -> bool:
    """
    Envía un ping a MongoDB para validar la conectividad.
    Lanza ServerSelectionTimeoutError si el servidor no responde.
    """
    await _state.client.admin.command("ping")
    return True


def get_database() -> AsyncIOMotorDatabase:
    """Retorna la instancia de la base de datos activa."""
    if _state.db is None:
        raise RuntimeError("Base de datos no inicializada. Llama a connect_db() primero.")
    return _state.db


def get_collection(name: str) -> AsyncIOMotorCollection:
    """Acceso directo a una colección por nombre."""
    return get_database()[name]


# Accesores semánticos para las colecciones principales
def users_collection() -> AsyncIOMotorCollection:
    return get_collection("users")


def alerts_collection() -> AsyncIOMotorCollection:
    return get_collection("alerts")


def sources_collection() -> AsyncIOMotorCollection:
    return get_collection("sources")


def articles_collection() -> AsyncIOMotorCollection:
    return get_collection("articles")
