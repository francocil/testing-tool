"""
Tests para routes/usuario.py

Cubre:
- Listar usuarios
- Obtener usuario por ID
- Crear usuario
- Actualizar usuario
- Eliminar usuario

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.usuario import Usuario
from models.rol import Rol


# ============================================================
# HELPERS
# ============================================================

def crear_rol(db, nombre="tester"):
    """
    Devuelve un rol existente o lo crea si no existe.
    Evita errores UNIQUE constraint failed: rol.nombre
    """
    rol = db.query(Rol).filter_by(nombre=nombre).first()
    if rol:
        return rol

    rol = Rol(nombre=nombre)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


def crear_usuario_en_db(db, nombre="Juan", email=None, rol_nombre="tester"):
    """
    Crea un usuario válido en la base de datos.
    Si no se pasa email, se genera uno único automáticamente.
    """

    # Generar email único si no se especifica
    if email is None:
        email = f"{nombre.lower().replace(' ', '_')}@test.com"

    rol = crear_rol(db, rol_nombre)

    usuario = Usuario(
        nombre=nombre,
        email=email,
        rol_id=rol.id,
        password_hash="hash123"
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_usuarios(client, db):
    crear_usuario_en_db(db, nombre="User 1")
    crear_usuario_en_db(db, nombre="User 2")

    resp = client.get("/api/v1/usuario/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nombre"] == "User 1"


def test_obtener_usuario_por_id(client, db):
    usuario = crear_usuario_en_db(db, nombre="Usuario Único")

    resp = client.get(f"/api/v1/usuario/{usuario.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == usuario.id
    assert data["nombre"] == "Usuario Único"


def test_obtener_usuario_inexistente(client):
    resp = client.get("/api/v1/usuario/9999")
    assert resp.status_code == 404


def test_crear_usuario(client, db):
    rol = crear_rol(db, "tester")

    payload = {
        "nombre": "Nuevo Usuario",
        "email": "nuevo@test.com",
        "rol_id": rol.id,
        "password": "123456"
    }

    resp = client.post("/api/v1/usuario/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "Nuevo Usuario"
    assert data["email"] == "nuevo@test.com"


def test_actualizar_usuario(client, db):
    usuario = crear_usuario_en_db(db, nombre="Viejo Nombre")

    payload = {
        "nombre": "Nombre Actualizado",
        "email": usuario.email,
        "rol_id": usuario.rol_id
    }

    resp = client.put(f"/api/v1/usuario/{usuario.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "Nombre Actualizado"


def test_actualizar_usuario_inexistente(client, db):
    rol = crear_rol(db)

    payload = {
        "nombre": "Nada",
        "email": "nada@test.com",
        "rol_id": rol.id
    }

    resp = client.put("/api/v1/usuario/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_usuario(client, db):
    usuario = crear_usuario_en_db(db)

    resp = client.delete(f"/api/v1/usuario/{usuario.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/usuario/{usuario.id}")
    assert resp2.status_code == 404
