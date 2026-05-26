"""
Tests para routes/rol.py

Cubre:
- Listar roles
- Obtener rol por ID
- Crear rol
- Actualizar rol
- Eliminar rol

IMPORTANTE:
Tu router suele usar el prefix:
    /api/v1/roles

Y los endpoints típicos son:
    GET    /roles/
    GET    /roles/{id}
    POST   /roles/
    PUT    /roles/{id}
    DELETE /roles/{id}

Si tu router usa otro prefix, ajustá las URLs en los tests.
"""

import pytest
from models.rol import Rol


# ============================================================
# HELPERS
# ============================================================

def crear_rol_en_db(db, nombre="Tester"):
    """
    Crea un rol válido según tu modelo real.
    """
    rol = Rol(nombre=nombre)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_roles(client, db):
    crear_rol_en_db(db, "Admin")
    crear_rol_en_db(db, "Tester")

    resp = client.get("/api/v1/roles/")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 2
    assert {"Admin", "Tester"}.issubset({r["nombre"] for r in data})


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_rol_por_id(client, db):
    rol = crear_rol_en_db(db, "Developer")

    resp = client.get(f"/api/v1/roles/{rol.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == rol.id
    assert data["nombre"] == "Developer"


def test_obtener_rol_inexistente(client):
    resp = client.get("/api/v1/roles/9999")
    assert resp.status_code == 404


def test_crear_rol(client, db):
    payload = {"nombre": "NuevoRol"}

    resp = client.post("/api/v1/roles/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "NuevoRol"


def test_actualizar_rol(client, db):
    rol = crear_rol_en_db(db, "Temporal")

    payload = {"nombre": "Actualizado"}

    resp = client.put(f"/api/v1/roles/{rol.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "Actualizado"


def test_actualizar_rol_inexistente(client):
    payload = {"nombre": "Nada"}

    resp = client.put("/api/v1/roles/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_rol(client, db):
    rol = crear_rol_en_db(db, "Eliminar")

    resp = client.delete(f"/api/v1/roles/{rol.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/roles/{rol.id}")
    assert resp2.status_code == 404
