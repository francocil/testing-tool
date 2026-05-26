"""
Tests para services/caso_prueba.py

Cubre:
- get_casos_prueba
- get_caso_prueba
- create_caso_prueba
- update_caso_prueba
- delete_caso_prueba

Validando:
- Nombre único por módulo
- Manejo de errores 404 y 409
- Actualización parcial
"""

import pytest
from fastapi import HTTPException

from services.caso_prueba import (
    get_casos_prueba,
    get_caso_prueba,
    create_caso_prueba,
    update_caso_prueba,
    delete_caso_prueba,
)

from services.proyecto import create_proyecto
from services.modulo import create_modulo

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate, CasoPruebaUpdate

from models.caso_prueba import CasoPrueba


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
    caso = CasoPrueba(
        modulo_id=modulo_id,
        nombre=nombre,
        objetivo="Objetivo",
        porcentaje_aceptacion=80.0
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


# ============================================================
# TESTS GET
# ============================================================

def test_get_casos_prueba(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    crear_caso_en_db(db, m.id, "A")
    crear_caso_en_db(db, m.id, "B")

    casos = get_casos_prueba(db)
    assert len(casos) == 2
    assert {c.nombre for c in casos} == {"A", "B"}


def test_get_caso_prueba_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)

    resultado = get_caso_prueba(db, caso.id)
    assert resultado.id == caso.id
    assert resultado.nombre == caso.nombre


def test_get_caso_prueba_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_caso_prueba(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Caso de prueba no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_caso_prueba(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    data = CasoPruebaCreate(
        modulo_id=m.id,
        nombre="Caso 1",
        objetivo="Objetivo",
        porcentaje_aceptacion=90.0
    )

    caso = create_caso_prueba(db, data)

    assert caso.id is not None
    assert caso.modulo_id == m.id
    assert caso.nombre == "Caso 1"
    assert caso.porcentaje_aceptacion == 90.0


def test_create_caso_prueba_nombre_duplicado(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    crear_caso_en_db(db, m.id, "Duplicado")

    data = CasoPruebaCreate(
        modulo_id=m.id,
        nombre="Duplicado",
        objetivo="X",
        porcentaje_aceptacion=80.0
    )

    with pytest.raises(HTTPException) as exc:
        create_caso_prueba(db, data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un caso de prueba con ese nombre en este módulo"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_caso_prueba(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id, "Original")

    data = CasoPruebaUpdate(
        nombre="Nuevo",
        objetivo="Actualizado",
        porcentaje_aceptacion=95.0
    )

    actualizado = update_caso_prueba(db, caso.id, data)

    assert actualizado.nombre == "Nuevo"
    assert actualizado.objetivo == "Actualizado"
    assert actualizado.porcentaje_aceptacion == 95.0


def test_update_caso_prueba_nombre_duplicado(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    crear_caso_en_db(db, m.id, "A")
    caso = crear_caso_en_db(db, m.id, "B")

    data = CasoPruebaUpdate(nombre="A")

    with pytest.raises(HTTPException) as exc:
        update_caso_prueba(db, caso.id, data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro caso de prueba con ese nombre en este módulo"


def test_update_caso_prueba_inexistente(db):
    data = CasoPruebaUpdate(nombre="X")

    with pytest.raises(HTTPException) as exc:
        update_caso_prueba(db, 9999, data)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_caso_prueba(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)

    delete_caso_prueba(db, caso.id)

    with pytest.raises(HTTPException):
        get_caso_prueba(db, caso.id)


def test_delete_caso_prueba_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_caso_prueba(db, 9999)

    assert exc.value.status_code == 404
