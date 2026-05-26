"""
Tests para services/paso.py

Cubre:
- get_pasos
- get_paso
- create_paso
- update_paso
- delete_paso

Validando:
- Orden único por caso
- Actualización parcial
- Manejo correcto de errores HTTP
"""

import pytest
from fastapi import HTTPException

from services.paso import (
    get_pasos,
    get_paso,
    create_paso,
    update_paso,
    delete_paso,
)
from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.paso import PasoCreate, PasoUpdate
from models.paso import Paso


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto X"):
    return create_proyecto(
        db,
        ProyectoCreate(
            nombre=nombre,
            objetivo_general="Objetivo",
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


def crear_paso_en_db(db, caso_id, orden=1, descripcion="Paso test"):
    paso = Paso(
        caso_id=caso_id,
        orden=orden,
        descripcion=descripcion
    )
    db.add(paso)
    db.commit()
    db.refresh(paso)
    return paso


# ============================================================
# TESTS GET
# ============================================================

def test_get_pasos(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)

    crear_paso_en_db(db, c.id, 1)
    crear_paso_en_db(db, c.id, 2)

    pasos = get_pasos(db)
    assert len(pasos) == 2
    assert {p.orden for p in pasos} == {1, 2}


def test_get_paso_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id, 1)

    resultado = get_paso(db, paso.id)
    assert resultado.id == paso.id
    assert resultado.orden == 1


def test_get_paso_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_paso(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Paso no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)

    data = PasoCreate(
        caso_id=c.id,
        descripcion="Primer paso",
        orden=1
    )

    paso = create_paso(db, data)

    assert paso.id is not None
    assert paso.caso_id == c.id
    assert paso.descripcion == "Primer paso"
    assert paso.orden == 1


def test_create_paso_orden_duplicado(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)

    crear_paso_en_db(db, c.id, 1)

    with pytest.raises(HTTPException) as exc:
        create_paso(
            db,
            PasoCreate(
                caso_id=c.id,
                descripcion="Duplicado",
                orden=1
            )
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un paso con ese orden en este caso"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id, 1)

    data = PasoUpdate(
        descripcion="Actualizado",
        orden=2
    )

    actualizado = update_paso(db, paso.id, data)

    assert actualizado.descripcion == "Actualizado"
    assert actualizado.orden == 2


def test_update_paso_orden_duplicado(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)

    crear_paso_en_db(db, c.id, 1)
    paso = crear_paso_en_db(db, c.id, 2)

    with pytest.raises(HTTPException) as exc:
        update_paso(
            db,
            paso.id,
            PasoUpdate(orden=1)
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro paso con ese orden en este caso"


def test_update_paso_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        update_paso(db, 9999, PasoUpdate(descripcion="X"))

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)

    delete_paso(db, paso.id)

    with pytest.raises(HTTPException):
        get_paso(db, paso.id)


def test_delete_paso_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_paso(db, 9999)

    assert exc.value.status_code == 404
