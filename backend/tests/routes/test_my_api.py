"""
Tests para routes/my_api.py

Cubre:
- Listar APIs
- Obtener API por ID
- Crear API
- Actualizar API
- Eliminar API
- Listar parámetros asociados a una API

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from models.my_api import Api
from models.objeto_parametro import ObjetoParametro
from models.paso import Paso


# ============================================================
# HELPERS
# ============================================================

def crear_api_en_db(db, nombre="API Test", metodo="GET", endpoint="https://x.com"):
    """
    Crea una API válida en la base de datos.
    """
    api = Api(nombre=nombre, metodo=metodo, endpoint=endpoint)
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


def crear_parametro_en_db(db, api_id):
    """
    Crea un parámetro asociado a una API y a un Paso real.
    Esto es obligatorio porque paso_id es NOT NULL.
    """

    # Crear un paso dummy asociado a un caso ficticio
    paso = Paso(caso_id=1, orden=1, descripcion="Paso para API")
    db.add(paso)
    db.commit()
    db.refresh(paso)

    param = ObjetoParametro(
        paso_id=paso.id,
        api_id=api_id,
        tipo="query",
        nombre="id",
        valor_entrada="123",
        valor_esperado="$.data.id"
    )
    db.add(param)
    db.commit()
    db.refresh(param)
    return param



# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_apis(client, db):
    crear_api_en_db(db, "API 1")
    crear_api_en_db(db, "API 2")

    resp = client.get("/api/v1/apis/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nombre"] == "API 1"


def test_obtener_api_por_id(client, db):
    api = crear_api_en_db(db, "API Unica")

    resp = client.get(f"/api/v1/apis/{api.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == api.id
    assert data["nombre"] == "API Unica"


def test_obtener_api_inexistente(client):
    resp = client.get("/api/v1/apis/9999")
    assert resp.status_code == 404


def test_crear_api(client, db):
    payload = {
        "nombre": "Nueva API",
        "metodo": "POST",
        "endpoint": "https://nuevo.com"
    }

    resp = client.post("/api/v1/apis/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["nombre"] == "Nueva API"
    assert data["metodo"] == "POST"


def test_actualizar_api(client, db):
    api = crear_api_en_db(db, "Vieja API")

    payload = {
        "nombre": "API Actualizada",
        "metodo": "PUT",
        "endpoint": "https://actualizado.com"
    }

    resp = client.put(f"/api/v1/apis/{api.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["nombre"] == "API Actualizada"
    assert data["metodo"] == "PUT"


def test_actualizar_api_inexistente(client):
    payload = {
        "nombre": "Nada",
        "metodo": "GET",
        "endpoint": "https://x.com"
    }

    resp = client.put("/api/v1/apis/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_api(client, db):
    api = crear_api_en_db(db)

    resp = client.delete(f"/api/v1/apis/{api.id}")
    assert resp.status_code == 204

    # Verificar que ya no existe
    resp2 = client.get(f"/api/v1/apis/{api.id}")
    assert resp2.status_code == 404


# ============================================================
# TESTS PARÁMETROS DE API
# ============================================================

def test_listar_parametros_de_api(client, db):
    api = crear_api_en_db(db)
    crear_parametro_en_db(db, api.id)

    resp = client.get(f"/api/v1/apis/{api.id}/parametros")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["nombre"] == "id"
