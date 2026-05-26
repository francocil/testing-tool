"""
Tests para services/modulo.py

Cubre:
- get_modulos
- get_modulos_por_proyecto
- get_modulo
- create_modulo
- update_modulo
- delete_modulo

Validando:
- Nombres únicos por proyecto
- Actualización de campos
- Manejo correcto de errores HTTP
"""

import pytest
from fastapi import HTTPException

from services.modulo import (
    get_modulos,
    get_modulos_por_proyecto,
    get_modulo,
    create_modulo,
    update_modulo,
    delete_modulo,
)
from services.proyecto import create_proyecto
from schemas.modulo import ModuloCreate, ModuloUpdate
from schemas.proyecto import ProyectoCreate
from models.modulo import Modulo


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


def crear_modulo_en_db(
    db,
    proyecto_id,
    nombre="Modulo Test",
    tipo_interfaz="API",
    tipo_gui="web",
    descripcion="desc"
):
    modulo = Modulo(
        proyecto_id=proyecto_id,
        nombre=nombre,
        tipo_interfaz=tipo_interfaz,
        tipo_gui=tipo_gui,
        descripcion=descripcion
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return modulo


# ============================================================
# TESTS GET
# ============================================================

def test_get_modulos(db):
    p = crear_proyecto_en_db(db)
    crear_modulo_en_db(db, p.id, "A")
    crear_modulo_en_db(db, p.id, "B")

    modulos = get_modulos(db)
    assert len(modulos) == 2
    assert {m.nombre for m in modulos} == {"A", "B"}


def test_get_modulos_por_proyecto(db):
    p1 = crear_proyecto_en_db(db, "P1")
    p2 = crear_proyecto_en_db(db, "P2")

    crear_modulo_en_db(db, p1.id, "M1")
    crear_modulo_en_db(db, p1.id, "M2")
    crear_modulo_en_db(db, p2.id, "M3")

    modulos_p1 = get_modulos_por_proyecto(db, p1.id)
    assert len(modulos_p1) == 2
    assert {m.nombre for m in modulos_p1} == {"M1", "M2"}

    modulos_p2 = get_modulos_por_proyecto(db, p2.id)
    assert len(modulos_p2) == 1
    assert modulos_p2[0].nombre == "M3"


def test_get_modulo_existente(db):
    p = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, p.id, "Modulo X")

    resultado = get_modulo(db, modulo.id)
    assert resultado.id == modulo.id
    assert resultado.nombre == "Modulo X"


def test_get_modulo_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_modulo(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Módulo no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_modulo(db):
    p = crear_proyecto_en_db(db)

    data = ModuloCreate(
        proyecto_id=p.id,
        nombre="Nuevo Modulo",
        tipo_interfaz="API",
        tipo_gui="web",
        descripcion="desc"
    )

    modulo = create_modulo(db, data)

    assert modulo.id is not None
    assert modulo.nombre == "Nuevo Modulo"
    assert modulo.tipo_interfaz == "API"
    assert modulo.tipo_gui == "web"
    assert modulo.descripcion == "desc"


def test_create_modulo_duplicado_en_mismo_proyecto(db):
    p = crear_proyecto_en_db(db)

    crear_modulo_en_db(db, p.id, "Duplicado")

    with pytest.raises(HTTPException) as exc:
        create_modulo(
            db,
            ModuloCreate(
                proyecto_id=p.id,
                nombre="Duplicado",
                tipo_interfaz="API",
                tipo_gui="web",
                descripcion="x"
            )
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe un módulo con ese nombre en este proyecto"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_modulo(db):
    p = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, p.id, "Original")

    data = ModuloUpdate(
        nombre="Actualizado",
        tipo_interfaz="SQL",
        tipo_gui="desktop",
        descripcion="Nueva desc"
    )

    actualizado = update_modulo(db, modulo.id, data)

    assert actualizado.nombre == "Actualizado"
    assert actualizado.tipo_interfaz == "SQL"
    assert actualizado.tipo_gui == "desktop"
    assert actualizado.descripcion == "Nueva desc"


def test_update_modulo_nombre_duplicado(db):
    p = crear_proyecto_en_db(db)

    crear_modulo_en_db(db, p.id, "Existente")
    modulo = crear_modulo_en_db(db, p.id, "Editable")

    with pytest.raises(HTTPException) as exc:
        update_modulo(
            db,
            modulo.id,
            ModuloUpdate(nombre="Existente")
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Ya existe otro módulo con ese nombre en este proyecto"


def test_update_modulo_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        update_modulo(db, 9999, ModuloUpdate(nombre="X"))

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_modulo(db):
    p = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, p.id)

    delete_modulo(db, modulo.id)

    with pytest.raises(HTTPException):
        get_modulo(db, modulo.id)


def test_delete_modulo_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_modulo(db, 9999)

    assert exc.value.status_code == 404
