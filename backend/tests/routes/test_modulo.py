"""
Tests para routes/modulo.py

Cubre:
- Listar módulos
- Obtener módulo por ID
- Crear módulo
- Actualizar módulo
- Eliminar módulo

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.modulo import Modulo
from models.proyecto import Proyecto


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto Base"):
    """
    Crea un proyecto válido en la base de datos.
    Los módulos requieren un proyecto existente.
    """
    proyecto = Proyecto(
        nombre=nombre,
        objetivo_general="Objetivo general",
        contexto="Contexto"
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def crear_modulo_en_db(db, proyecto_id, nombre="Modulo Test"):
    """
    Crea un módulo válido asociado a un proyecto real.
    """
    modulo = Modulo(
        proyecto_id=proyecto_id,
        nombre=nombre,
        tipo_interfaz="API",
        tipo_gui="web",
        descripcion="Descripción del módulo"
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return modulo


# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_modulos(client, db):
    proyecto = crear_proyecto_en_db(db)

    crear_modulo_en_db(db, proyecto.id, "Modulo 1")
    crear_modulo_en_db(db, proyecto.id, "Modulo 2")

    resp = client.get("/api/v1/modulos/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nombre"] == "Modulo 1"


def test_obtener_modulo_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id, "Modulo Único")

    resp = client.get(f"/api/v1/modulos/{modulo.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == modulo.id
    assert data["nombre"] == "Modulo Único"


def test_obtener_modulo_inexistente(client):
    resp = client.get("/api/v1/modulos/9999")
    assert resp.status_code == 404


def test_crear_modulo(client, db):
    proyecto = crear_proyecto_en_db(db)

    payload = {
        "proyecto_id": proyecto.id,
        "nombre": "Nuevo Modulo",
        "tipo_interfaz": "API",
        "tipo_gui": "web",
        "descripcion": "Descripción"
    }

    resp = client.post("/api/v1/modulos/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "Nuevo Modulo"
    assert data["proyecto_id"] == proyecto.id


def test_actualizar_modulo(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id, "Modulo Viejo")

    payload = {
        "proyecto_id": proyecto.id,
        "nombre": "Modulo Actualizado",
        "tipo_interfaz": modulo.tipo_interfaz,
        "tipo_gui": modulo.tipo_gui,
        "descripcion": modulo.descripcion
    }

    resp = client.put(f"/api/v1/modulos/{modulo.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "Modulo Actualizado"


def test_actualizar_modulo_inexistente(client, db):
    proyecto = crear_proyecto_en_db(db)

    payload = {
        "proyecto_id": proyecto.id,
        "nombre": "Nada",
        "tipo_interfaz": "API",
        "tipo_gui": "web",
        "descripcion": "X"
    }

    resp = client.put("/api/v1/modulos/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_modulo(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)

    resp = client.delete(f"/api/v1/modulos/{modulo.id}")
    assert resp.status_code == 204

    # Verificar que ya no existe
    resp2 = client.get(f"/api/v1/modulos/{modulo.id}")
    assert resp2.status_code == 404
