"""
Router /api/v1/users — CRUD de usuarios.
Solo accesible por gestores (role: gestor_newsradar).
"""
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import hash_password, require_gestor
from db.database import users_collection
from models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _doc_to_response(doc: dict) -> UserResponse:
    """Convierte un documento MongoDB en UserResponse."""
    return UserResponse(
        id=str(doc["_id"]),
        email=doc["email"],
        name=doc["name"],
        role=doc["role"],
        active=doc.get("active", True),
        preferences=doc.get("preferences", {}),
        createdAt=doc.get("createdAt", datetime.utcnow()),
    )


async def _get_user_or_404(user_id: str) -> dict:
    """Busca un usuario por ID o lanza 404."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    col = users_collection()
    doc = await col.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return doc


# ------------------------------------------------------------------ #
# GET /api/v1/users
# ------------------------------------------------------------------ #

@router.get(
    "",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Devuelve todos los usuarios del sistema. Solo accesible por gestores.",
)
async def list_users(
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=20, ge=1, le=100, description="Máximo de registros a devolver"),
    role: Optional[str] = Query(default=None, description="Filtrar por rol"),
    _: dict = Depends(require_gestor),
) -> List[UserResponse]:
    col = users_collection()
    query: dict = {}
    if role:
        query["role"] = role

    cursor = col.find(query).skip(skip).limit(limit).sort("createdAt", -1)
    docs = await cursor.to_list(length=limit)
    return [_doc_to_response(d) for d in docs]


# ------------------------------------------------------------------ #
# POST /api/v1/users
# ------------------------------------------------------------------ #

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Solo accesible por gestores.",
)
async def create_user(
    body: UserCreate,
    _: dict = Depends(require_gestor),
) -> UserResponse:
    col = users_collection()

    if await col.find_one({"email": body.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el email {body.email}",
        )

    now = datetime.utcnow()
    doc = {
        "email": body.email,
        "password": hash_password(body.password),
        "name": body.name,
        "role": body.role.value,
        "active": True,
        "preferences": body.preferences.model_dump(),
        "createdAt": now,
        "lastLogin": None,
    }
    result = await col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _doc_to_response(doc)


# ------------------------------------------------------------------ #
# GET /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Devuelve un usuario concreto por su ID. Solo accesible por gestores.",
)
async def get_user(
    user_id: str,
    _: dict = Depends(require_gestor),
) -> UserResponse:
    doc = await _get_user_or_404(user_id)
    return _doc_to_response(doc)


# ------------------------------------------------------------------ #
# PUT /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza los campos indicados de un usuario. Solo accesible por gestores.",
)
async def update_user(
    user_id: str,
    body: UserUpdate,
    _: dict = Depends(require_gestor),
) -> UserResponse:
    await _get_user_or_404(user_id)
    col = users_collection()

    updates: dict = {}
    if body.email is not None:
        if await col.find_one({"email": body.email, "_id": {"$ne": ObjectId(user_id)}}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El email {body.email} ya está en uso",
            )
        updates["email"] = body.email
    if body.name is not None:
        updates["name"] = body.name
    if body.password is not None:
        updates["password"] = hash_password(body.password)
    if body.role is not None:
        updates["role"] = body.role.value
    if body.active is not None:
        updates["active"] = body.active
    if body.preferences is not None:
        updates["preferences"] = body.preferences.model_dump()

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se proporcionaron campos para actualizar",
        )

    updates["updatedAt"] = datetime.utcnow()
    await col.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    doc = await col.find_one({"_id": ObjectId(user_id)})
    return _doc_to_response(doc)


# ------------------------------------------------------------------ #
# DELETE /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID. Solo accesible por gestores.",
)
async def delete_user(
    user_id: str,
    _: dict = Depends(require_gestor),
) -> None:
    doc = await _get_user_or_404(user_id)

    if doc.get("email") == "admin@newsradar.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se puede eliminar el usuario administrador del sistema",
        )

    col = users_collection()
    await col.delete_one({"_id": ObjectId(user_id)})
