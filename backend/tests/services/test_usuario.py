"""
Tests para services/usuario.py

Cubre:
- get_usuarios
- get_usuario
- create_usuario
- update_usuario
- delete_usuario

Validando:
- Emails únicos
- Hash de contraseña (bcrypt)
- Actualización de campos opcionales
- Manejo correcto de errores HTTP
"""

import pytest
import bcrypt
from fastapi import HTTPException

from services.usuario import (
    get_usuarios,
    get_usuario,
    create_usuario,
    update_usuario,
    delete_usuario,
)
from services.rol import create_rol
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from schemas.rol import RolCreate
from models.usuario import Usuario
from core.security import hash_password


# ============================================================
# HELPERS
# ============================================================

def crear_rol_en_db(db, nombre="Tester"):
    return create_rol(db, RolCreate(nombre=nombre))


def crear_usuario_en_db(db, nombre="Juan", email="juan@test.com", password="1234", rol_id=1):
    usuario = Usuario(
        nombre=nombre,
        email=email,
        password_hash=hash_password(password),
        rol_id=rol_id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# ============================================================
# TESTS GET
# ============================================================

def test_get_usuarios(db):
    rol = crear_rol_en_db(db)
    crear_usuario_en_db(db, "A", "a@test.com", "1234", rol.id)
    crear_usuario_en_db(db, "B", "b@test.com", "1234", rol.id)

    usuarios = get_usuarios(db)
    assert len(usuarios) == 2
    assert {u.email for u in usuarios} == {"a@test.com", "b@test.com"}


def test_get_usuario_existente(db):
    rol = crear_rol_en_db(db)
    usuario = crear_usuario_en_db(db, "Juan", "juan@test.com", "1234", rol.id)

    resultado = get_usuario(db, usuario.id)
    assert resultado.id == usuario.id
    assert resultado.email == "juan@test.com"


def test_get_usuario_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_usuario(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuario no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_usuario(db):
    rol = crear_rol_en_db(db)

    data = UsuarioCreate(
        nombre="Nuevo",
        email="nuevo@test.com",
        password="secreto",
        rol_id=rol.id
    )

    usuario = create_usuario(db, data)

    assert usuario.id is not None
    assert usuario.email == "nuevo@test.com"
    assert usuario.password_hash != "secreto"
    assert bcrypt.checkpw("secreto".encode(), usuario.password_hash.encode())


def test_create_usuario_email_duplicado(db):
    rol = crear_rol_en_db(db)
    crear_usuario_en_db(db, "Juan", "juan@test.com", "1234", rol.id)

    with pytest.raises(HTTPException) as exc:
        create_usuario(
            db,
            UsuarioCreate(
                nombre="Otro",
                email="juan@test.com",
                password="abcd",
                rol_id=rol.id
            )
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un usuario con ese email"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_usuario(db):
    rol1 = crear_rol_en_db(db, "Tester")
    rol2 = crear_rol_en_db(db, "Admin")

    usuario = crear_usuario_en_db(db, "Juan", "juan@test.com", "1234", rol1.id)

    data = UsuarioUpdate(
        nombre="Juan Actualizado",
        email="nuevo@test.com",
        password="nueva",
        rol_id=rol2.id,
        activo=False
    )

    actualizado = update_usuario(db, usuario.id, data)

    assert actualizado.nombre == "Juan Actualizado"
    assert actualizado.email == "nuevo@test.com"
    assert bcrypt.checkpw("nueva".encode(), actualizado.password_hash.encode())
    assert actualizado.rol_id == rol2.id
    assert actualizado.activo is False


def test_update_usuario_email_duplicado(db):
    rol = crear_rol_en_db(db)

    u1 = crear_usuario_en_db(db, "A", "a@test.com", "1234", rol.id)
    crear_usuario_en_db(db, "B", "b@test.com", "1234", rol.id)

    with pytest.raises(HTTPException) as exc:
        update_usuario(db, u1.id, UsuarioUpdate(email="b@test.com"))

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro usuario con ese email"


def test_update_usuario_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        update_usuario(db, 9999, UsuarioUpdate(nombre="X"))

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_usuario(db):
    rol = crear_rol_en_db(db)
    usuario = crear_usuario_en_db(db, "Juan", "juan@test.com", "1234", rol.id)

    delete_usuario(db, usuario.id)

    with pytest.raises(HTTPException):
        get_usuario(db, usuario.id)


def test_delete_usuario_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_usuario(db, 9999)

    assert exc.value.status_code == 404
