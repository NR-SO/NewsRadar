"""
Configuración centralizada de la aplicación NEWSRADAR.
Lee variables de entorno con valores por defecto para desarrollo.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base de datos MongoDB
    MONGODB_URL: str = "mongodb://admin:password@localhost:27017/newsradar_db?authSource=admin"
    DATABASE_NAME: str = "newsradar_db"

    # Entorno y modo
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Seguridad / JWT
    SECRET_KEY: str = "newsradar-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Paginación
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Límites de negocio
    MAX_ALERTS_PER_MANAGER: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
