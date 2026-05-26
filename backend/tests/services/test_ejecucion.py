"""
Tests para services/ejecucion.py

Cubre:
- get_ejecucion
- get_ejecuciones_por_caso
- create_ejecucion
- update_ejecucion
- delete_ejecucion

Validando:
- FK a CasoPrueba
- FK a Usuario
- Manejo de errores 404
"""

import pytest
from fastapi import HTTPException

from services.ejecucion import (
    get_ejecucion,
    get_ejecuciones_por_caso,
    create_ejecucion,
    update_ejecucion,
    delete_ejecucion,
)

from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from services.usuario import create_usuario

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.usuario import UsuarioCreate
from schemas.ejecucion import EjecucionCreate, EjecucionUpdate

from models.ejecucion import Ejecucion


# ============================================================
# HELPERS
# ============================================================

def crear_usuario_en_db(db, nombre="Tester"):
    return create_usuario(
        db,
        UsuarioCreate(
            nombre=nombre,
            email=f"{nombre.lower()}@test.com",
            password="1234",
            rol_id=1  # Asumimos rol válido
        )
    )


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


def crear_ejecucion_en_db(db, caso_id, usuario_id):
    ejec = Ejecucion(
        caso_id=caso_id,
        usuario_id=usuario_id,
        modo="automatico",
        estado="pendiente",
        resultado_global=None,
        porcentaje_aceptacion=None,
        fecha_fin=None
    )
    db.add(ejec)
    db.commit()
    db.refresh(ejec)
    return ejec


# ============================================================
# TESTS GET
# ============================================================

def test_get_ejecucion_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)

    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    resultado = get_ejecucion(db, ejec.id)
    assert resultado.id == ejec.id
    assert resultado.caso_id == caso.id
    assert resultado.usuario_id == usuario.id


def test_get_ejecucion_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_ejecucion(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Ejecución no encontrada"


# ============================================================
# TESTS LISTAR
# ============================================================

def test_get_ejecuciones_por_caso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)

    crear_ejecucion_en_db(db, caso.id, usuario.id)
    crear_ejecucion_en_db(db, caso.id, usuario.id)

    ejecuciones = get_ejecuciones_por_caso(db, caso.id)
    assert len(ejecuciones) == 2


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_ejecucion(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)

    data = EjecucionCreate(
        caso_id=caso.id,
        usuario_id=usuario.id,
        modo="automatico",
        resultado_global=None,
        porcentaje_aceptacion=None
    )

    ejec = create_ejecucion(db, data)

    assert ejec.id is not None
    assert ejec.caso_id == caso.id
    assert ejec.usuario_id == usuario.id
    assert ejec.estado == "pendiente"


def test_create_ejecucion_caso_inexistente(db):
    usuario = crear_usuario_en_db(db)

    data = EjecucionCreate(
        caso_id=9999,
        usuario_id=usuario.id,
        modo="automatico",
        resultado_global=None,
        porcentaje_aceptacion=None
    )

    with pytest.raises(HTTPException) as exc:
        create_ejecucion(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Caso de prueba no encontrado"


def test_create_ejecucion_usuario_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)

    data = EjecucionCreate(
        caso_id=caso.id,
        usuario_id=9999,
        modo="automatico",
        resultado_global=None,
        porcentaje_aceptacion=None
    )

    with pytest.raises(HTTPException) as exc:
        create_ejecucion(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuario no encontrado"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_ejecucion(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)

    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    data = EjecucionUpdate(
        modo="mixto",
        estado="en_progreso",
        resultado_global="ok",
        porcentaje_aceptacion=100.0,
        fecha_fin=None
    )

    actualizado = update_ejecucion(db, ejec.id, data)

    assert actualizado.modo == "mixto"
    assert actualizado.estado == "en_progreso"
    assert actualizado.resultado_global == "ok"
    assert actualizado.porcentaje_aceptacion == 100.0


def test_update_ejecucion_inexistente(db):
    data = EjecucionUpdate(estado="finalizado")

    with pytest.raises(HTTPException) as exc:
        update_ejecucion(db, 9999, data)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_ejecucion(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)

    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    delete_ejecucion(db, ejec.id)

    with pytest.raises(HTTPException):
        get_ejecucion(db, ejec.id)


def test_delete_ejecucion_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_ejecucion(db, 9999)

    assert exc.value.status_code == 404
