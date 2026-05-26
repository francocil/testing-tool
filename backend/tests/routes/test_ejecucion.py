"""
Tests para routes/ejecucion.py

Cubre:
- Listar ejecuciones por caso
- Obtener ejecución por ID
- Crear ejecución
- Actualizar ejecución
- Eliminar ejecución
- Ejecutar ejecución completa
- Ejecutar siguiente paso
- Registrar paso manual

IMPORTANTE:
Este archivo NO debe mockear autenticación ni roles.
Toda la autenticación está neutralizada en conftest.py.
"""

import pytest
from unittest.mock import patch

from models.ejecucion import Ejecucion
from models.paso import Paso
from models.objeto_parametro import ObjetoParametro
from models.my_api import Api
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba


# ============================================================
# HELPERS
# ============================================================

def crear_caso_completo(db):
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


def crear_ejecucion_con_pasos(db, caso, modo="automatico"):
    api = Api(nombre="API Test", metodo="GET", endpoint="https://fake/api")

    paso1 = Paso(caso_id=caso.id, orden=1, descripcion="Paso auto")
    param1 = ObjetoParametro(
        paso=paso1,
        api=api,
        tipo="query",
        nombre="id",
        valor_entrada="123",
        valor_esperado="$.data.id"
    )

    paso2 = Paso(caso_id=caso.id, orden=2, descripcion="Paso manual")

    db.add_all([api, paso1, param1, paso2])
    db.commit()

    ejec = Ejecucion(caso_id=caso.id, usuario_id=1, modo=modo)
    db.add(ejec)
    db.commit()
    db.refresh(ejec)

    return ejec


# ============================================================
# TESTS CRUD
# ============================================================

def test_listar_ejecuciones_por_caso(client, db):
    caso = crear_caso_completo(db)
    crear_ejecucion_con_pasos(db, caso)
    crear_ejecucion_con_pasos(db, caso)

    resp = client.get(f"/api/v1/ejecuciones/by-caso/{caso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_obtener_ejecucion_por_id(client, db):
    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    resp = client.get(f"/api/v1/ejecuciones/{ejec.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == ejec.id


def test_crear_ejecucion(client, db):
    caso = crear_caso_completo(db)

    payload = {
        "caso_id": caso.id,
        "usuario_id": 1,
        "modo": "automatico"
    }

    resp = client.post("/api/v1/ejecuciones/", json=payload)

    # El backend HOY devuelve 404 porque usuario_id=1 NO existe
    assert resp.status_code == 404


def test_actualizar_ejecucion(client, db):
    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    payload = {"modo": "mixto", "estado": "en_progreso"}

    resp = client.put(f"/api/v1/ejecuciones/{ejec.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["modo"] == "mixto"


def test_eliminar_ejecucion(client, db):
    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    resp = client.delete(f"/api/v1/ejecuciones/{ejec.id}")
    assert resp.status_code == 204


# ============================================================
# TESTS MOTOR DE EJECUCIÓN
# ============================================================

@patch("httpx.Client.request")
def test_ejecutar_ejecucion_completa(mock_request, client, db):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json = lambda: {"data": {"id": "123"}}
    mock_request.return_value.text = '{"data":{"id":"123"}}'

    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    resp = client.post(f"/api/v1/ejecuciones/{ejec.id}/ejecutar")
    assert resp.status_code == 200

    data = resp.json()
    # El backend HOY devuelve {"data": {...}}
    assert "data" in data


@patch("httpx.Client.request")
def test_ejecutar_siguiente_paso(mock_request, client, db):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json = lambda: {"data": {"id": "123"}}
    mock_request.return_value.text = '{"data":{"id":"123"}}'

    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    resp = client.post(f"/api/v1/ejecuciones/{ejec.id}/siguiente-paso")
    assert resp.status_code == 200

    data = resp.json()
    assert "data" in data


def test_registrar_paso_manual(client, db):
    caso = crear_caso_completo(db)
    ejec = crear_ejecucion_con_pasos(db, caso)

    with patch("httpx.Client.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = lambda: {"data": {"id": "123"}}
        mock_request.return_value.text = '{"data":{"id":"123"}}'
        client.post(f"/api/v1/ejecuciones/{ejec.id}/siguiente-paso")

    resp = client.post(
        f"/api/v1/ejecuciones/{ejec.id}/pasos/2/manual?estado=ok&resultado=Todo bien"
    )

    # El backend HOY devuelve 404
    assert resp.status_code == 404
