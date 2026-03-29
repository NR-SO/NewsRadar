"""
Tests para los esquemas User y Role — S2-03
Validan modelos Pydantic, permisos y seed del admin.
"""

import pytest
from pydantic import ValidationError

from src.backend.models.user import UserCreate, UserInDB, UserRole, UserUpdate
from src.backend.models.role import (
    ROLES,
    Permission,
    get_permissions,
    has_permission,
)


# ============================================================
# UserRole enum
# ============================================================

def test_user_role_values():
    assert UserRole.gestor_newsradar == "gestor_newsradar"
    assert UserRole.lector == "lector"


def test_user_role_only_two_values():
    assert set(UserRole) == {UserRole.gestor_newsradar, UserRole.lector}


# ============================================================
# UserCreate
# ============================================================

def test_user_create_default_role_is_lector():
    u = UserCreate(email="test@test.com", password="secret", name="Test")
    assert u.role == UserRole.lector


def test_user_create_accepts_gestor():
    u = UserCreate(
        email="gestor@test.com",
        password="secret",
        name="Gestor",
        role=UserRole.gestor_newsradar,
    )
    assert u.role == UserRole.gestor_newsradar


def test_user_create_rejects_invalid_role():
    with pytest.raises(ValidationError):
        UserCreate(email="x@x.com", password="s", name="X", role="admin")


def test_user_create_requires_email():
    with pytest.raises(ValidationError):
        UserCreate(password="secret", name="Test")


def test_user_create_requires_valid_email_format():
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="secret", name="Test")


# ============================================================
# UserUpdate (todos los campos opcionales)
# ============================================================

def test_user_update_all_fields_optional():
    u = UserUpdate()
    assert u.email is None
    assert u.name is None
    assert u.password is None
    assert u.role is None
    assert u.active is None


def test_user_update_partial():
    u = UserUpdate(name="Nuevo Nombre")
    assert u.name == "Nuevo Nombre"
    assert u.email is None


def test_user_update_rejects_invalid_role():
    with pytest.raises(ValidationError):
        UserUpdate(role="superadmin")


# ============================================================
# Role definitions
# ============================================================

def test_roles_dict_contains_both_roles():
    assert "gestor_newsradar" in ROLES
    assert "lector" in ROLES


def test_gestor_has_user_write_permission():
    assert has_permission("gestor_newsradar", Permission.users_write)


def test_gestor_has_source_write_permission():
    assert has_permission("gestor_newsradar", Permission.sources_write)


def test_lector_cannot_write_users():
    assert not has_permission("lector", Permission.users_write)


def test_lector_cannot_write_sources():
    assert not has_permission("lector", Permission.sources_write)


def test_lector_can_read_articles():
    assert has_permission("lector", Permission.articles_read)


def test_gestor_permissions_superset_of_lector():
    lector_perms = set(get_permissions("lector"))
    gestor_perms = set(get_permissions("gestor_newsradar"))
    assert lector_perms.issubset(gestor_perms)


def test_unknown_role_returns_empty_permissions():
    assert get_permissions("superadmin") == []


def test_unknown_role_has_no_permission():
    assert not has_permission("superadmin", Permission.articles_read)
