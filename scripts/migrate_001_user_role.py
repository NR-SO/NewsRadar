"""
Migración 001 — Esquema User y Role
====================================
Idempotente: puede ejecutarse varias veces sin efectos secundarios.

Acciones:
  1. Aplica el validador JSON Schema a la colección 'users' (crea si no existe).
  2. Crea/actualiza la colección 'roles' con los documentos canónicos.
  3. Garantiza los índices necesarios en 'users'.
  4. Inserta el usuario admin inicial si no existe.

Uso:
    # Dentro del contenedor backend:
    docker exec -it newsradar-backend python /app/scripts/migrate_001_user_role.py

    # O directamente con MongoDB accesible:
    MONGODB_URL=mongodb://admin:password@localhost:27017 python scripts/migrate_001_user_role.py
"""

import os
import sys
from datetime import datetime

from passlib.context import CryptContext
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid

MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://admin:password@localhost:27017/newsradar_db?authSource=admin",
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "newsradar_db")

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

USER_SCHEMA_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email", "password", "name", "role"],
        "properties": {
            "email":    {"bsonType": "string"},
            "password": {"bsonType": "string"},
            "name":     {"bsonType": "string"},
            "role":     {"enum": ["gestor_newsradar", "lector"]},
            "active":   {"bsonType": "bool"},
            "preferences": {
                "bsonType": "object",
                "properties": {
                    "iptcSubscriptions":   {"bsonType": "array"},
                    "sourceSubscriptions": {"bsonType": "array"},
                    "alertsEnabled":       {"bsonType": "bool"},
                    "emailNotifications":  {"bsonType": "bool"},
                    "language":            {"enum": ["es", "en"]},
                },
            },
            "createdAt": {"bsonType": "date"},
            "lastLogin": {"bsonType": ["date", "null"]},
        },
    }
}

ROLES_SEED = [
    {
        "name": "gestor_newsradar",
        "description": "Gestor de contenidos: administra usuarios, fuentes y alertas.",
        "permissions": [
            "users:read", "users:write",
            "sources:read", "sources:write",
            "alerts:read", "alerts:write",
            "articles:read", "notifications:read",
        ],
    },
    {
        "name": "lector",
        "description": "Lector: acceso de solo lectura a noticias, alertas y notificaciones.",
        "permissions": [
            "alerts:read", "articles:read", "notifications:read",
        ],
    },
]

ADMIN_USER = {
    "email": "admin@newsradar.com",
    "password_plain": "admin123",
    "name": "Admin Manager",
    "role": "gestor_newsradar",
}


def migrate_users_collection(db) -> None:
    print("→ Colección 'users'...")
    try:
        db.create_collection("users")
        print("  Colección creada.")
    except CollectionInvalid:
        print("  Ya existe, actualizando validador...")

    db.command({
        "collMod": "users",
        "validator": USER_SCHEMA_VALIDATOR,
        "validationLevel": "moderate",
    })

    db["users"].create_index([("email", ASCENDING)], unique=True, name="idx_users_email")
    print("  ✓ Validador y índice email aplicados.")


def migrate_roles_collection(db) -> None:
    print("→ Colección 'roles'...")
    try:
        db.create_collection("roles")
        print("  Colección creada.")
    except CollectionInvalid:
        print("  Ya existe.")

    db["roles"].create_index([("name", ASCENDING)], unique=True, name="idx_roles_name")

    for role in ROLES_SEED:
        db["roles"].update_one(
            {"name": role["name"]},
            {"$set": {**role, "updatedAt": datetime.utcnow()}},
            upsert=True,
        )
        print(f"  ✓ Rol upserted: {role['name']}")


def seed_admin_user(db) -> None:
    print("→ Usuario admin inicial...")
    col = db["users"]
    if col.find_one({"email": ADMIN_USER["email"]}):
        print(f"  Ya existe: {ADMIN_USER['email']}")
        return

    col.insert_one({
        "email": ADMIN_USER["email"],
        "password": pwd_ctx.hash(ADMIN_USER["password_plain"]),
        "name": ADMIN_USER["name"],
        "role": ADMIN_USER["role"],
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
    })
    print(f"  ✓ Admin creado: {ADMIN_USER['email']} (contraseña: {ADMIN_USER['password_plain']})")


def main() -> None:
    print("=" * 60)
    print("Migración 001 — Esquema User y Role")
    print(f"BD: {DATABASE_NAME}")
    print("=" * 60)

    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("✓ Conexión establecida\n")
    except Exception as exc:
        print(f"✗ Error al conectar: {exc}", file=sys.stderr)
        sys.exit(1)

    db = client[DATABASE_NAME]

    migrate_users_collection(db)
    print()
    migrate_roles_collection(db)
    print()
    seed_admin_user(db)

    print("\n" + "=" * 60)
    print("✓ Migración 001 completada")
    print(f"  users : {db['users'].count_documents({})} documento(s)")
    print(f"  roles : {db['roles'].count_documents({})} documento(s)")
    print("=" * 60)

    client.close()


if __name__ == "__main__":
    main()
