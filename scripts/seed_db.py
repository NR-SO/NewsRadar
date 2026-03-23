"""
Script de seed para NEWSRADAR.
Inserta usuarios, alertas y fuentes iniciales en MongoDB usando bcrypt para contraseñas.

Uso:
    # Dentro del contenedor backend:
    docker exec -it newsradar-backend python /app/scripts/seed_db.py

    # O directamente (requiere MongoDB accesible):
    MONGODB_URL=mongodb://admin:password@localhost:27017/newsradar_db?authSource=admin python scripts/seed_db.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from passlib.context import CryptContext
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# ------------------------------------------------------------------ #
# Configuración
# ------------------------------------------------------------------ #
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://admin:password@localhost:27017/newsradar_db?authSource=admin",
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "newsradar_db")

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ruta al seed.json (relativa al script o al workdir del contenedor)
SEED_FILE = Path(__file__).parent.parent / "data" / "seed.json"


def load_seed() -> dict:
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_users(db, seed_data: dict) -> int:
    col = db["users"]
    created = 0
    for u in seed_data.get("users", []):
        if col.find_one({"email": u["email"]}):
            print(f"  Usuario ya existe: {u['email']}")
            continue
        doc = {
            "email": u["email"],
            "password": pwd_ctx.hash(u["password_plain"]),
            "name": u["name"],
            "role": u["role"],  # gestor_newsradar | lector
            "active": True,
            "preferences": u.get("preferences", {
                "iptcSubscriptions": [],
                "sourceSubscriptions": [],
                "alertsEnabled": True,
                "emailNotifications": True,
                "language": "es",
            }),
            "createdAt": datetime.utcnow(),
            "lastLogin": None,
        }
        col.insert_one(doc)
        created += 1
        print(f"  ✓ Usuario creado: {u['email']} ({u['role']})")
    return created


def seed_alerts(db, seed_data: dict) -> int:
    users_col = db["users"]
    alerts_col = db["alerts"]
    created = 0
    for a in seed_data.get("alerts", []):
        owner = users_col.find_one({"email": a["owner_email"]})
        if not owner:
            print(f"  ⚠  Propietario no encontrado para alerta '{a['name']}': {a['owner_email']}")
            continue
        if alerts_col.find_one({"name": a["name"], "ownerId": str(owner["_id"])}):
            print(f"  Alerta ya existe: {a['name']}")
            continue
        doc = {
            "name": a["name"],
            "ownerId": str(owner["_id"]),
            "keywords": a["keywords"],
            "iptcTopics": a.get("iptcTopics", []),
            "active": a.get("active", True),
            "matchCount": 0,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
        alerts_col.insert_one(doc)
        created += 1
        print(f"  ✓ Alerta creada: {a['name']}")
    return created


def main() -> None:
    print("=" * 60)
    print("NEWSRADAR — Script de seed de base de datos")
    print(f"Conectando a: {MONGODB_URL[:40]}...")
    print("=" * 60)

    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("✓ Conexión a MongoDB establecida\n")
    except Exception as exc:
        print(f"✗ Error al conectar a MongoDB: {exc}", file=sys.stderr)
        sys.exit(1)

    db = client[DATABASE_NAME]

    try:
        seed_data = load_seed()
    except FileNotFoundError:
        print(f"✗ No se encontró {SEED_FILE}", file=sys.stderr)
        sys.exit(1)

    print("→ Creando usuarios...")
    u_count = seed_users(db, seed_data)

    print("\n→ Creando alertas de ejemplo...")
    a_count = seed_alerts(db, seed_data)

    print("\n" + "=" * 60)
    print(f"✓ Seed completado: {u_count} usuario(s), {a_count} alerta(s)")
    print("=" * 60)

    # Resumen del estado de la BD
    print("\nEstado de la base de datos:")
    for col in ["users", "alerts", "sources", "articles"]:
        count = db[col].count_documents({})
        print(f"  {col:12s}: {count:5d} documento(s)")

    client.close()


if __name__ == "__main__":
    main()
