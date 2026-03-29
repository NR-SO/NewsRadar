"""Modelo de datos para Roles del sistema NEWSRADAR."""
from enum import Enum
from typing import List

from pydantic import BaseModel


class Permission(str, Enum):
    # Gestión de usuarios (solo gestor_newsradar)
    users_read = "users:read"
    users_write = "users:write"
    # Gestión de fuentes RSS
    sources_read = "sources:read"
    sources_write = "sources:write"
    # Gestión de alertas
    alerts_read = "alerts:read"
    alerts_write = "alerts:write"
    # Lectura de noticias (todos)
    articles_read = "articles:read"
    # Notificaciones
    notifications_read = "notifications:read"


# Mapa de permisos por rol
ROLE_PERMISSIONS: dict = {
    "gestor_newsradar": [
        Permission.users_read,
        Permission.users_write,
        Permission.sources_read,
        Permission.sources_write,
        Permission.alerts_read,
        Permission.alerts_write,
        Permission.articles_read,
        Permission.notifications_read,
    ],
    "lector": [
        Permission.alerts_read,
        Permission.articles_read,
        Permission.notifications_read,
    ],
}


class RoleDefinition(BaseModel):
    """Representa un rol del sistema con sus permisos asociados."""
    name: str
    description: str
    permissions: List[Permission]


# Definiciones canónicas de los roles del sistema
ROLES: dict[str, RoleDefinition] = {
    "gestor_newsradar": RoleDefinition(
        name="gestor_newsradar",
        description="Gestor de contenidos: puede administrar usuarios, fuentes y alertas.",
        permissions=ROLE_PERMISSIONS["gestor_newsradar"],
    ),
    "lector": RoleDefinition(
        name="lector",
        description="Lector: acceso de solo lectura a noticias, alertas y notificaciones.",
        permissions=ROLE_PERMISSIONS["lector"],
    ),
}


def get_permissions(role: str) -> List[Permission]:
    """Devuelve los permisos asociados a un rol. Lista vacía si el rol no existe."""
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(role: str, permission: Permission) -> bool:
    """Comprueba si un rol tiene un permiso concreto."""
    return permission in ROLE_PERMISSIONS.get(role, [])
