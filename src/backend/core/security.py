"""
Capa de seguridad JWT para NEWSRADAR.
Proporciona creación/verificación de tokens y dependencias FastAPI
para proteger endpoints según rol.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

ALGORITHM = "HS256"

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=True)


# ------------------------------------------------------------------ #
# Contraseñas
# ------------------------------------------------------------------ #

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


# ------------------------------------------------------------------ #
# JWT
# ------------------------------------------------------------------ #

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decodifica y valida el token JWT. Lanza HTTPException 401 si es inválido."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ------------------------------------------------------------------ #
# Dependencias FastAPI
# ------------------------------------------------------------------ #

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Dependencia que extrae y valida el JWT del header Authorization.
    Devuelve el payload del token como dict con al menos 'sub' y 'role'.
    """
    payload = decode_access_token(credentials.credentials)
    email: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")

    if not email or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token mal formado: faltan campos sub/role",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"email": email, "role": role}


async def require_gestor(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependencia que garantiza que el usuario autenticado tenga
    el rol gestor_newsradar. Lanza 403 si no es así.
    """
    if current_user.get("role") != "gestor_newsradar":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a gestores",
        )
    return current_user
