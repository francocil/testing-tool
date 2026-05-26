"""
Tests para routes/objeto_parametro.py

Cubre:
- Listar parámetros por paso
- Listar parámetros por API
- Obtener parámetro por ID
- Crear parámetro
- Actualizar parámetro
- Eliminar parámetro

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.objeto_parametro import ObjetoParametro
from models.my_api import Api
from models.paso import Paso
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db):
    proyecto = Proyecto(
        nombre="Proyecto Test",
        objetivo_general="Objetivo",
        contexto="Contexto"
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


def crear_caso_en_db(db, modulo_id):
    caso = CasoPrueba(
        nombre="Caso Test",
        objetivo="Objetivo",
        modulo_id=modulo_id,
        porcentaje_aceptacion=100.0
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


def crear_paso_en_db(db, caso_id):
    paso = Paso(
        caso_id=caso_id,
        orden=1,
        descripcion="Paso Test"
    )
    db.add(paso)
    db.commit()
    db.refresh(paso)
    return paso


def crear_api_en_db(db):
    api = Api(
        nombre="API Test",
        metodo="GET",
        endpoint="https://fake.com"
    )
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


def crear_parametro_en_db(db, paso_id, api_id, nombre="id"):
    param = ObjetoParametro(
        paso_id=paso_id,
        api_id=api_id,
        tipo="query",
        nombre=nombre,
        valor_entrada="123",
        valor_esperado="$.data.id"
    )
    db.add(param)
    db.commit()
    db.refresh(param)
    return param


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_parametros_por_paso(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    crear_parametro_en_db(db, paso.id, api.id, nombre="p1")
    crear_parametro_en_db(db, paso.id, api.id, nombre="p2")

    resp = client.get(f"/api/v1/objetos-parametros/by-paso/{paso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {p["nombre"] for p in data} == {"p1", "p2"}


def test_listar_parametros_por_api(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    crear_parametro_en_db(db, paso.id, api.id, nombre="p1")
    crear_parametro_en_db(db, paso.id, api.id, nombre="p2")

    resp = client.get(f"/api/v1/objetos-parametros/by-api/{api.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {p["nombre"] for p in data} == {"p1", "p2"}


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_parametro_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    param = crear_parametro_en_db(db, paso.id, api.id)

    resp = client.get(f"/api/v1/objetos-parametros/{param.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == param.id
    assert data["nombre"] == "id"


def test_obtener_parametro_inexistente(client):
    resp = client.get("/api/v1/objetos-parametros/9999")
    assert resp.status_code == 404


def test_crear_parametro(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    payload = {
        "paso_id": paso.id,
        "api_id": api.id,
        "tipo": "query",
        "nombre": "nuevo",
        "valor_entrada": "abc",
        "valor_esperado": "$.data.value"
    }

    resp = client.post("/api/v1/objetos-parametros/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "nuevo"
    assert data["paso_id"] == paso.id
    assert data["api_id"] == api.id


def test_actualizar_parametro(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    param = crear_parametro_en_db(db, paso.id, api.id)

    payload = {
        "paso_id": paso.id,
        "api_id": api.id,
        "tipo": "query",
        "nombre": "actualizado",
        "valor_entrada": "999",
        "valor_esperado": "$.data.new"
    }

    resp = client.put(f"/api/v1/objetos-parametros/{param.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "actualizado"
    assert data["valor_entrada"] == "999"


def test_actualizar_parametro_inexistente(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    payload = {
        "paso_id": paso.id,
        "api_id": api.id,
        "tipo": "query",
        "nombre": "x",
        "valor_entrada": "y",
        "valor_esperado": "z"
    }

    resp = client.put("/api/v1/objetos-parametros/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_parametro(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    api = crear_api_en_db(db)

    param = crear_parametro_en_db(db, paso.id, api.id)

    resp = client.delete(f"/api/v1/objetos-parametros/{param.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/objetos-parametros/{param.id}")
    assert resp2.status_code == 404
