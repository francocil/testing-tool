"""
Tests para services/caso_prueba_version.py

Cubre:
- get_caso_prueba_versiones
- get_caso_prueba_version
- create_caso_prueba_version
- update_caso_prueba_version
- delete_caso_prueba_version

Validando:
- Manejo de errores 404
"""

import pytest
from fastapi import HTTPException

from services.caso_prueba_version import (
    get_caso_prueba_versiones,
    get_caso_prueba_version,
    create_caso_prueba_version,
    update_caso_prueba_version,
    delete_caso_prueba_version,
)

from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.caso_prueba_version import CasoPruebaVersionCreate, CasoPruebaVersionUpdate

from models.caso_prueba_version import CasoPruebaVersion


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto X"):
    return create_proyecto(
        db,
        ProyectoCreate(
            nombre=nombre,
            objetivo_general="Objetivo general",
            contexto="Contexto"
        )
    )


def crear_modulo_en_db(db, proyecto_id, nombre="Modulo X"):
    return create_modulo(
        db,
        ModuloCreate(
            proyecto_id=proyecto_id,
            nombre=nombre,
            tipo_interfaz="API",
            tipo_gui="web",
            descripcion="desc"
        )
    )


def crear_caso_en_db(db, modulo_id, nombre="Caso X"):
    return create_caso_prueba(
        db,
        CasoPruebaCreate(
            modulo_id=modulo_id,
            nombre=nombre,
            objetivo="Objetivo",
            porcentaje_aceptacion=80.0
        )
    )


def crear_version_en_db(db, caso_id, nro=1, objetivo="v1", pct=80.0):
    version = CasoPruebaVersion(
        caso_id=caso_id,
        nro_version=nro,
        objetivo=objetivo,
        porcentaje_aceptacion=pct
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


# ============================================================
# TESTS GET
# ============================================================

def test_get_caso_prueba_versiones(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)

    crear_version_en_db(db, caso.id, 1)
    crear_version_en_db(db, caso.id, 2)

    versiones = get_caso_prueba_versiones(db)
    assert len(versiones) == 2
    assert {v.nro_version for v in versiones} == {1, 2}


def test_get_caso_prueba_version_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    version = crear_version_en_db(db, caso.id)

    resultado = get_caso_prueba_version(db, version.id)
    assert resultado.id == version.id
    assert resultado.nro_version == 1


def test_get_caso_prueba_version_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_caso_prueba_version(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Versión de caso de prueba no encontrada"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_caso_prueba_version(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)

    data = CasoPruebaVersionCreate(
        caso_id=caso.id,
        nro_version=1,
        objetivo="Inicial",
        porcentaje_aceptacion=90.0
    )

    version = create_caso_prueba_version(db, data)

    assert version.id is not None
    assert version.caso_id == caso.id
    assert version.nro_version == 1
    assert version.objetivo == "Inicial"
    assert version.porcentaje_aceptacion == 90.0


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_caso_prueba_version(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    version = crear_version_en_db(db, caso.id)

    data = CasoPruebaVersionUpdate(
        objetivo="Actualizado",
        porcentaje_aceptacion=95.0
    )

    actualizado = update_caso_prueba_version(db, version.id, data)

    assert actualizado.objetivo == "Actualizado"
    assert actualizado.porcentaje_aceptacion == 95.0


def test_update_caso_prueba_version_inexistente(db):
    data = CasoPruebaVersionUpdate(objetivo="X")

    with pytest.raises(HTTPException) as exc:
        update_caso_prueba_version(db, 9999, data)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_caso_prueba_version(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    version = crear_version_en_db(db, caso.id)

    delete_caso_prueba_version(db, version.id)

    with pytest.raises(HTTPException):
        get_caso_prueba_version(db, version.id)


def test_delete_caso_prueba_version_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_caso_prueba_version(db, 9999)

    assert exc.value.status_code == 404
