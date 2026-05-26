"""
Tests para services/rol.py

Cubre:
- get_roles
- get_rol
- create_rol
- update_rol
- delete_rol

El objetivo es validar la lógica interna del servicio sin pasar por rutas.
"""

import pytest
from fastapi import HTTPException

from services.rol import (
    get_roles,
    get_rol,
    create_rol,
    update_rol,
    delete_rol,
)
from schemas.rol import RolCreate, RolUpdate
from models.rol import Rol


# ============================================================
# HELPERS
# ============================================================

def crear_rol_en_db(db, nombre="Tester"):
    rol = Rol(nombre=nombre)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


# ============================================================
# TESTS GET
# ============================================================

def test_get_roles(db):
    crear_rol_en_db(db, "Admin")
    crear_rol_en_db(db, "Tester")

    roles = get_roles(db)
    assert len(roles) == 2
    assert {r.nombre for r in roles} == {"Admin", "Tester"}


def test_get_rol_existente(db):
    rol = crear_rol_en_db(db, "Admin")

    resultado = get_rol(db, rol.id)
    assert resultado.id == rol.id
    assert resultado.nombre == "Admin"


def test_get_rol_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_rol(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Rol no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_rol(db):
    data = RolCreate(nombre="NuevoRol")

    rol = create_rol(db, data)

    assert rol.id is not None
    assert rol.nombre == "NuevoRol"


def test_create_rol_duplicado(db):
    crear_rol_en_db(db, "Admin")

    with pytest.raises(HTTPException) as exc:
        create_rol(db, RolCreate(nombre="Admin"))

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un rol con ese nombre"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_rol(db):
    rol = crear_rol_en_db(db, "Tester")

    data = RolUpdate(nombre="QA Lead")
    actualizado = update_rol(db, rol.id, data)

    assert actualizado.nombre == "QA Lead"


def test_update_rol_duplicado(db):
    crear_rol_en_db(db, "Admin")
    rol = crear_rol_en_db(db, "Tester")

    with pytest.raises(HTTPException) as exc:
        update_rol(db, rol.id, RolUpdate(nombre="Admin"))

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro rol con ese nombre"


def test_update_rol_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        update_rol(db, 9999, RolUpdate(nombre="X"))

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_rol(db):
    rol = crear_rol_en_db(db, "Tester")

    delete_rol(db, rol.id)

    with pytest.raises(HTTPException):
        get_rol(db, rol.id)


def test_delete_rol_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_rol(db, 9999)

    assert exc.value.status_code == 404
