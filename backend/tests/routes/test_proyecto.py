"""
Tests para routes/proyecto.py

Cubre:
- Listar proyectos
- Obtener proyecto por ID
- Crear proyecto
- Actualizar proyecto
- Eliminar proyecto

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.proyecto import Proyecto


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto Test"):
    """
    Crea un proyecto válido en la base de datos.
    """
    proyecto = Proyecto(
        nombre=nombre,
        objetivo_general="Objetivo general",
        contexto="Contexto del proyecto"
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_proyectos(client, db):
    """
    Verifica que el endpoint devuelva todos los proyectos existentes.
    """
    crear_proyecto_en_db(db, "Proyecto 1")
    crear_proyecto_en_db(db, "Proyecto 2")

    resp = client.get("/api/v1/proyectos/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nombre"] == "Proyecto 1"


def test_obtener_proyecto_por_id(client, db):
    """
    Verifica que se pueda obtener un proyecto existente por ID.
    """
    proyecto = crear_proyecto_en_db(db, "Proyecto Único")

    resp = client.get(f"/api/v1/proyectos/{proyecto.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == proyecto.id
    assert data["nombre"] == "Proyecto Único"


def test_obtener_proyecto_inexistente(client):
    """
    Verifica que obtener un proyecto inexistente devuelva 404.
    """
    resp = client.get("/api/v1/proyectos/9999")
    assert resp.status_code == 404


def test_crear_proyecto(client):
    """
    Verifica que el endpoint permita crear un proyecto nuevo.
    """
    payload = {
        "nombre": "Nuevo Proyecto",
        "objetivo_general": "Objetivo",
        "contexto": "Contexto"
    }

    resp = client.post("/api/v1/proyectos/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "Nuevo Proyecto"
    assert data["objetivo_general"] == "Objetivo"


def test_actualizar_proyecto(client, db):
    """
    Verifica que se pueda actualizar un proyecto existente.
    """
    proyecto = crear_proyecto_en_db(db, "Proyecto Viejo")

    payload = {
        "nombre": "Proyecto Actualizado",
        "objetivo_general": proyecto.objetivo_general,
        "contexto": proyecto.contexto
    }

    resp = client.put(f"/api/v1/proyectos/{proyecto.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "Proyecto Actualizado"


def test_actualizar_proyecto_inexistente(client):
    """
    Verifica que actualizar un proyecto inexistente devuelva 404.
    """
    payload = {
        "nombre": "Nada",
        "objetivo_general": "X",
        "contexto": "Y"
    }

    resp = client.put("/api/v1/proyectos/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_proyecto(client, db):
    """
    Verifica que se pueda eliminar un proyecto existente.
    """
    proyecto = crear_proyecto_en_db(db)

    resp = client.delete(f"/api/v1/proyectos/{proyecto.id}")
    assert resp.status_code == 204

    # Verificar que ya no existe
    resp2 = client.get(f"/api/v1/proyectos/{proyecto.id}")
    assert resp2.status_code == 404
