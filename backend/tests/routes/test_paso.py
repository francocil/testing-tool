"""
Tests para routes/paso.py

Cubre:
- Listar pasos
- Obtener paso por ID
- Crear paso
- Actualizar paso
- Eliminar paso

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest

from models.paso import Paso
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba


# ============================================================
# HELPERS
# ============================================================

def crear_caso_real(db):
    """
    Crea Proyecto → Módulo → CasoPrueba.
    Es necesario porque el backend NO permite crear pasos
    si el caso_id no existe realmente.
    """
    proyecto = Proyecto(
        nombre="Proyecto Test",
        objetivo_general="Obj",
        contexto="Ctx"
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)

    modulo = Modulo(
        proyecto_id=proyecto.id,
        nombre="Modulo Test",
        tipo_interfaz="API",
        tipo_gui="web",
        descripcion="desc"
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)

    caso = CasoPrueba(
        nombre="Caso Test",
        objetivo="Objetivo",
        modulo_id=modulo.id,
        porcentaje_aceptacion=100.0
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)

    return caso


def crear_paso_en_db(db, caso_id, orden=1, descripcion="Paso Test"):
    """
    Crea un paso válido asociado a un caso real.
    """
    paso = Paso(caso_id=caso_id, orden=orden, descripcion=descripcion)
    db.add(paso)
    db.commit()
    db.refresh(paso)
    return paso


# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_pasos(client, db):
    caso = crear_caso_real(db)

    crear_paso_en_db(db, caso.id, descripcion="Paso 1")
    crear_paso_en_db(db, caso.id, descripcion="Paso 2")

    resp = client.get("/api/v1/pasos/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["descripcion"] == "Paso 1"


def test_obtener_paso_por_id(client, db):
    caso = crear_caso_real(db)
    paso = crear_paso_en_db(db, caso.id, descripcion="Paso Único")

    resp = client.get(f"/api/v1/pasos/{paso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == paso.id
    assert data["descripcion"] == "Paso Único"


def test_obtener_paso_inexistente(client):
    resp = client.get("/api/v1/pasos/9999")
    assert resp.status_code == 404


def test_crear_paso(client, db):
    caso = crear_caso_real(db)

    payload = {
        "caso_id": caso.id,
        "orden": 1,
        "descripcion": "Nuevo Paso"
    }

    resp = client.post("/api/v1/pasos/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["descripcion"] == "Nuevo Paso"
    assert data["orden"] == 1


def test_actualizar_paso(client, db):
    caso = crear_caso_real(db)
    paso = crear_paso_en_db(db, caso.id, descripcion="Viejo Paso")

    payload = {
        "caso_id": paso.caso_id,
        "orden": paso.orden,
        "descripcion": "Paso Actualizado"
    }

    resp = client.put(f"/api/v1/pasos/{paso.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["descripcion"] == "Paso Actualizado"


def test_actualizar_paso_inexistente(client):
    payload = {
        "caso_id": 1,
        "orden": 1,
        "descripcion": "Nada"
    }

    resp = client.put("/api/v1/pasos/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_paso(client, db):
    caso = crear_caso_real(db)
    paso = crear_paso_en_db(db, caso.id)

    resp = client.delete(f"/api/v1/pasos/{paso.id}")
    assert resp.status_code == 204

    # Verificar que ya no existe
    resp2 = client.get(f"/api/v1/pasos/{paso.id}")
    assert resp2.status_code == 404
