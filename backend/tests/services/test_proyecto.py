"""
Tests para services/proyecto.py

Cubre:
- get_proyectos
- get_proyecto
- create_proyecto
- update_proyecto
- delete_proyecto

Validando:
- Nombres únicos
- Actualización de campos
- Manejo correcto de errores HTTP
"""

import pytest
from fastapi import HTTPException

from services.proyecto import (
    get_proyectos,
    get_proyecto,
    create_proyecto,
    update_proyecto,
    delete_proyecto,
)
from schemas.proyecto import ProyectoCreate, ProyectoUpdate
from models.proyecto import Proyecto


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(
    db,
    nombre="Proyecto Test",
    objetivo="Objetivo general",
    contexto="Contexto del proyecto"
):
    proyecto = Proyecto(
        nombre=nombre,
        objetivo_general=objetivo,
        contexto=contexto
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


# ============================================================
# TESTS GET
# ============================================================

def test_get_proyectos(db):
    crear_proyecto_en_db(db, "A")
    crear_proyecto_en_db(db, "B")

    proyectos = get_proyectos(db)
    assert len(proyectos) == 2
    assert {p.nombre for p in proyectos} == {"A", "B"}


def test_get_proyecto_existente(db):
    proyecto = crear_proyecto_en_db(db, "Proyecto X")

    resultado = get_proyecto(db, proyecto.id)
    assert resultado.id == proyecto.id
    assert resultado.nombre == "Proyecto X"


def test_get_proyecto_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_proyecto(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Proyecto no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_proyecto(db):
    data = ProyectoCreate(
        nombre="Nuevo Proyecto",
        objetivo_general="Objetivo",
        contexto="Contexto"
    )

    proyecto = create_proyecto(db, data)

    assert proyecto.id is not None
    assert proyecto.nombre == "Nuevo Proyecto"
    assert proyecto.objetivo_general == "Objetivo"
    assert proyecto.contexto == "Contexto"


def test_create_proyecto_duplicado(db):
    crear_proyecto_en_db(db, "Duplicado")

    with pytest.raises(HTTPException) as exc:
        create_proyecto(
            db,
            ProyectoCreate(
                nombre="Duplicado",
                objetivo_general="X",
                contexto="Y"
            )
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un proyecto con ese nombre"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_proyecto(db):
    proyecto = crear_proyecto_en_db(db, "Original")

    data = ProyectoUpdate(
        nombre="Actualizado",
        objetivo_general="Nuevo objetivo",
        contexto="Nuevo contexto"
    )

    actualizado = update_proyecto(db, proyecto.id, data)

    assert actualizado.nombre == "Actualizado"
    assert actualizado.objetivo_general == "Nuevo objetivo"
    assert actualizado.contexto == "Nuevo contexto"


def test_update_proyecto_nombre_duplicado(db):
    crear_proyecto_en_db(db, "Existente")
    proyecto = crear_proyecto_en_db(db, "Editable")

    with pytest.raises(HTTPException) as exc:
        update_proyecto(
            db,
            proyecto.id,
            ProyectoUpdate(nombre="Existente")
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro proyecto con ese nombre"


def test_update_proyecto_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        update_proyecto(db, 9999, ProyectoUpdate(nombre="X"))

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_proyecto(db):
    proyecto = crear_proyecto_en_db(db)

    delete_proyecto(db, proyecto.id)

    with pytest.raises(HTTPException):
        get_proyecto(db, proyecto.id)


def test_delete_proyecto_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_proyecto(db, 9999)

    assert exc.value.status_code == 404
