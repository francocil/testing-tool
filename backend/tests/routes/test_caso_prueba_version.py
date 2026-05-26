"""
Tests para routes/caso_prueba_version.py

Cubre:
- Listar versiones (filtradas por caso_id)
- Obtener versión por ID
- Crear versión
- Actualizar versión
- Eliminar versión

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/casos-prueba-versiones
NO existe /casos-prueba-version ni /casos-prueba-version/by-caso.
El listado general se obtiene con GET "/" y se filtra por query param.

ACLARACIÓN IMPORTANTE SOBRE UPDATE:
-----------------------------------
Tu servicio update_caso_prueba_version SOLO actualiza:
    - objetivo
    - porcentaje_aceptacion

NO actualiza:
    - nro_version
    - caso_id

Por lo tanto, los tests NO deben esperar cambios en esos campos.
"""

import pytest
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba
from models.caso_prueba_version import CasoPruebaVersion


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


def crear_version_en_db(db, caso_id, nro_version=1):
    """
    Tu modelo real usa:
        caso_id
        nro_version
        objetivo
        porcentaje_aceptacion
    """
    version = CasoPruebaVersion(
        caso_id=caso_id,
        nro_version=nro_version,
        objetivo="Objetivo versión",
        porcentaje_aceptacion=100.0
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_versiones_por_caso(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    crear_version_en_db(db, caso.id, nro_version=1)
    crear_version_en_db(db, caso.id, nro_version=2)

    resp = client.get(f"/api/v1/casos-prueba-versiones/?caso_id={caso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 2
    assert {v["nro_version"] for v in data} == {1, 2}


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_version_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    version = crear_version_en_db(db, caso.id, nro_version=1)

    resp = client.get(f"/api/v1/casos-prueba-versiones/{version.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == version.id
    assert data["nro_version"] == 1


def test_obtener_version_inexistente(client):
    resp = client.get("/api/v1/casos-prueba-versiones/9999")
    assert resp.status_code == 404


def test_crear_version(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    payload = {
        "caso_id": caso.id,
        "nro_version": 1,
        "objetivo": "Nueva versión",
        "porcentaje_aceptacion": 95.0
    }

    resp = client.post("/api/v1/casos-prueba-versiones/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["caso_id"] == caso.id
    assert data["nro_version"] == 1


def test_actualizar_version(client, db):
    """
    ACLARACIÓN:
    Tu servicio NO actualiza nro_version ni caso_id.
    Por eso este test SOLO valida los campos que sí se actualizan.
    """
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    version = crear_version_en_db(db, caso.id, nro_version=1)

    payload = {
        "caso_id": caso.id,            # NO se actualiza en el service
        "nro_version": 1,              # NO se actualiza en el service
        "objetivo": "Actualizado",     # SÍ se actualiza
        "porcentaje_aceptacion": 80.0  # SÍ se actualiza
    }

    resp = client.put(f"/api/v1/casos-prueba-versiones/{version.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()

    # Campos que NO cambian
    assert data["nro_version"] == 1
    assert data["caso_id"] == caso.id

    # Campos que SÍ cambian
    assert data["objetivo"] == "Actualizado"
    assert data["porcentaje_aceptacion"] == 80.0


def test_actualizar_version_inexistente(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    payload = {
        "caso_id": caso.id,
        "nro_version": 99,
        "objetivo": "Nada",
        "porcentaje_aceptacion": 50.0
    }

    resp = client.put("/api/v1/casos-prueba-versiones/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_version(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)

    version = crear_version_en_db(db, caso.id, nro_version=1)

    resp = client.delete(f"/api/v1/casos-prueba-versiones/{version.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/casos-prueba-versiones/{version.id}")
    assert resp2.status_code == 404
