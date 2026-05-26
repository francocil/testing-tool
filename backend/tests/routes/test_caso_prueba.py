"""
Tests para routes/caso_prueba.py

Cubre:
- Listar casos de prueba
- Obtener caso por ID
- Crear caso de prueba
- Actualizar caso de prueba
- Eliminar caso de prueba

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.caso_prueba import CasoPrueba
from models.modulo import Modulo
from models.proyecto import Proyecto


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto Test"):
    proyecto = Proyecto(
        nombre=nombre,
        objetivo_general="Objetivo del proyecto",
        contexto="Contexto del proyecto"
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def crear_modulo_en_db(db, proyecto_id):
    modulo = Modulo(
        proyecto_id=proyecto_id,
        nombre="Modulo Test",
        tipo_interfaz="API",
        tipo_gui="web",
        descripcion="desc"
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return modulo


def crear_caso_en_db(db, nombre="Caso Test"):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)

    caso = CasoPrueba(
        nombre=nombre,
        objetivo="Objetivo X",
        modulo_id=modulo.id,
        porcentaje_aceptacion=100.0
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


# ============================================================
# TESTS
# ============================================================

def test_listar_casos_prueba(client, db):
    crear_caso_en_db(db, "Caso 1")
    crear_caso_en_db(db, "Caso 2")

    resp = client.get("/api/v1/casos-prueba/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nombre"] == "Caso 1"


def test_obtener_caso_prueba_por_id(client, db):
    caso = crear_caso_en_db(db, "Caso Único")

    resp = client.get(f"/api/v1/casos-prueba/{caso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == caso.id
    assert data["nombre"] == "Caso Único"


def test_obtener_caso_prueba_inexistente(client):
    resp = client.get("/api/v1/casos-prueba/9999")
    assert resp.status_code == 404


def test_crear_caso_prueba(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)

    payload = {
        "nombre": "Nuevo Caso",
        "objetivo": "Objetivo del caso",
        "modulo_id": modulo.id,
        "porcentaje_aceptacion": 80.0
    }

    resp = client.post("/api/v1/casos-prueba/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "Nuevo Caso"
    assert data["objetivo"] == "Objetivo del caso"


def test_actualizar_caso_prueba(client, db):
    caso = crear_caso_en_db(db, "Caso Viejo")

    payload = {
        "nombre": "Caso Actualizado",
        "objetivo": "Nuevo objetivo"
    }

    resp = client.put(f"/api/v1/casos-prueba/{caso.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "Caso Actualizado"
    assert data["objetivo"] == "Nuevo objetivo"


def test_actualizar_caso_prueba_inexistente(client):
    payload = {
        "nombre": "Nada",
        "objetivo": "Nada"
    }

    resp = client.put("/api/v1/casos-prueba/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_caso_prueba(client, db):
    caso = crear_caso_en_db(db)

    resp = client.delete(f"/api/v1/casos-prueba/{caso.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/casos-prueba/{caso.id}")
    assert resp2.status_code == 404
