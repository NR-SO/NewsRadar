"""
Tests para GET/POST/PUT/DELETE /api/v1/users — S2-04
Usa tokens JWT reales para autenticación (sin DB real).
"""
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Importamos usando el path que carga el mismo módulo que usa el app
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src/backend"))

from core.security import create_access_token  # mismo módulo que usa el app
from src.backend.main import app

# ------------------------------------------------------------------ #
# Tokens de prueba
# ------------------------------------------------------------------ #

def _gestor_token() -> str:
    return create_access_token({"sub": "admin@newsradar.com", "role": "gestor_newsradar"})


def _lector_token() -> str:
    return create_access_token({"sub": "reader@newsradar.com", "role": "lector"})


def _expired_token() -> str:
    return create_access_token(
        {"sub": "admin@newsradar.com", "role": "gestor_newsradar"},
        expires_delta=timedelta(seconds=-1),
    )


# ------------------------------------------------------------------ #
# Fixtures
# ------------------------------------------------------------------ #

@pytest.fixture
def gestor_client():
    client = TestClient(app, raise_server_exceptions=False)
    client.headers.update({"Authorization": f"Bearer {_gestor_token()}"})
    return client


@pytest.fixture
def lector_client():
    client = TestClient(app, raise_server_exceptions=False)
    client.headers.update({"Authorization": f"Bearer {_lector_token()}"})
    return client


@pytest.fixture
def unauth_client():
    return TestClient(app, raise_server_exceptions=False)


# Documento MongoDB de ejemplo
SAMPLE_DOC = {
    "_id": MagicMock(__str__=lambda self: "64b0000000000000000000aa"),
    "email": "test@newsradar.com",
    "name": "Test User",
    "role": "lector",
    "active": True,
    "preferences": {
        "iptcSubscriptions": [],
        "sourceSubscriptions": [],
        "alertsEnabled": True,
        "emailNotifications": True,
        "language": "es",
    },
    "createdAt": "2024-01-01T00:00:00",
}


# ------------------------------------------------------------------ #
# GET /api/v1/users
# ------------------------------------------------------------------ #

def test_list_users_returns_200_for_gestor(gestor_client):
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=[])

    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find.return_value = mock_cursor
        response = gestor_client.get("/api/v1/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_users_returns_403_for_lector(lector_client):
    response = lector_client.get("/api/v1/users")
    assert response.status_code == 403


def test_list_users_returns_401_without_auth(unauth_client):
    response = unauth_client.get("/api/v1/users")
    assert response.status_code in (401, 403)


def test_list_users_returns_401_with_expired_token(unauth_client):
    unauth_client.headers.update({"Authorization": f"Bearer {_expired_token()}"})
    response = unauth_client.get("/api/v1/users")
    assert response.status_code == 401


# ------------------------------------------------------------------ #
# POST /api/v1/users
# ------------------------------------------------------------------ #

def test_create_user_returns_201(gestor_client):
    mock_result = MagicMock()
    mock_result.inserted_id = MagicMock(__str__=lambda self: "64b0000000000000000000bb")

    with patch("api.v1.users.hash_password", return_value="$2b$12$hashed"), \
         patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=None)
        mock_col.return_value.insert_one = AsyncMock(return_value=mock_result)

        response = gestor_client.post("/api/v1/users", json={
            "email": "nuevo@test.com",
            "password": "password123",
            "name": "Nuevo Usuario",
            "role": "lector",
        })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "nuevo@test.com"
    assert data["role"] == "lector"
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_returns_409_on_duplicate_email(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value={"email": "dup@test.com"})

        response = gestor_client.post("/api/v1/users", json={
            "email": "dup@test.com",
            "password": "password123",
            "name": "Duplicado",
        })

    assert response.status_code == 409


def test_create_user_returns_403_for_lector(lector_client):
    response = lector_client.post("/api/v1/users", json={
        "email": "x@test.com", "password": "pass", "name": "X",
    })
    assert response.status_code == 403


def test_create_user_rejects_invalid_role(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=None)
        response = gestor_client.post("/api/v1/users", json={
            "email": "x@test.com",
            "password": "pass",
            "name": "X",
            "role": "superadmin",
        })
    assert response.status_code == 422


# ------------------------------------------------------------------ #
# GET /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

def test_get_user_returns_200(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=SAMPLE_DOC)
        response = gestor_client.get("/api/v1/users/64b0000000000000000000aa")

    assert response.status_code == 200
    assert response.json()["email"] == "test@newsradar.com"


def test_get_user_returns_404_for_unknown_id(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=None)
        response = gestor_client.get("/api/v1/users/64b0000000000000000000ff")

    assert response.status_code == 404


def test_get_user_returns_404_for_invalid_id(gestor_client):
    response = gestor_client.get("/api/v1/users/not-a-valid-id")
    assert response.status_code == 404


def test_get_user_returns_403_for_lector(lector_client):
    response = lector_client.get("/api/v1/users/64b0000000000000000000aa")
    assert response.status_code == 403


# ------------------------------------------------------------------ #
# PUT /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

def test_update_user_returns_200(gestor_client):
    updated_doc = {**SAMPLE_DOC, "name": "Nombre Actualizado"}

    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(side_effect=[SAMPLE_DOC, updated_doc])
        mock_col.return_value.update_one = AsyncMock()

        response = gestor_client.put(
            "/api/v1/users/64b0000000000000000000aa",
            json={"name": "Nombre Actualizado"},
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Nombre Actualizado"


def test_update_user_returns_422_with_empty_body(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=SAMPLE_DOC)
        response = gestor_client.put(
            "/api/v1/users/64b0000000000000000000aa",
            json={},
        )

    assert response.status_code == 422


def test_update_user_returns_404_for_unknown(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=None)
        response = gestor_client.put(
            "/api/v1/users/64b0000000000000000000ff",
            json={"name": "X"},
        )

    assert response.status_code == 404


def test_update_user_returns_403_for_lector(lector_client):
    response = lector_client.put(
        "/api/v1/users/64b0000000000000000000aa",
        json={"name": "X"},
    )
    assert response.status_code == 403


# ------------------------------------------------------------------ #
# DELETE /api/v1/users/{user_id}
# ------------------------------------------------------------------ #

def test_delete_user_returns_204(gestor_client):
    deletable_doc = {**SAMPLE_DOC, "email": "otro@test.com"}

    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=deletable_doc)
        mock_col.return_value.delete_one = AsyncMock()
        response = gestor_client.delete("/api/v1/users/64b0000000000000000000aa")

    assert response.status_code == 204


def test_delete_admin_user_returns_403(gestor_client):
    admin_doc = {**SAMPLE_DOC, "email": "admin@newsradar.com"}

    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=admin_doc)
        response = gestor_client.delete("/api/v1/users/64b0000000000000000000aa")

    assert response.status_code == 403


def test_delete_user_returns_404_for_unknown(gestor_client):
    with patch("api.v1.users.users_collection") as mock_col:
        mock_col.return_value.find_one = AsyncMock(return_value=None)
        response = gestor_client.delete("/api/v1/users/64b0000000000000000000ff")

    assert response.status_code == 404


def test_delete_user_returns_403_for_lector(lector_client):
    response = lector_client.delete("/api/v1/users/64b0000000000000000000aa")
    assert response.status_code == 403
