"""
Tests para services/ejecucion_paso.py

Cubre:
- get_ejecucion_paso
- get_ejecuciones_paso_por_ejecucion
- create_ejecucion_paso
- update_ejecucion_paso
- delete_ejecucion_paso

Validando:
- FK a Ejecucion
- FK a Paso
- Manejo de errores 404
"""

import pytest
from fastapi import HTTPException

from services.ejecucion_paso import (
    get_ejecucion_paso,
    get_ejecuciones_paso_por_ejecucion,
    create_ejecucion_paso,
    update_ejecucion_paso,
    delete_ejecucion_paso,
)

from services.ejecucion import create_ejecucion
from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from services.paso import create_paso
from services.usuario import create_usuario

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.paso import PasoCreate
from schemas.usuario import UsuarioCreate
from schemas.ejecucion import EjecucionCreate
from schemas.ejecucion_paso import EjecucionPasoCreate, EjecucionPasoUpdate

from models.ejecucion_paso import EjecucionPaso


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
            rol_id=1
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


def crear_paso_en_db(db, caso_id, orden=1):
    return create_paso(
        db,
        PasoCreate(
            caso_id=caso_id,
            descripcion="Paso de prueba",
            orden=orden
        )
    )


def crear_ejecucion_en_db(db, caso_id, usuario_id):
    data = EjecucionCreate(
        caso_id=caso_id,
        usuario_id=usuario_id,
        modo="automatico",
        resultado_global=None,
        porcentaje_aceptacion=None
    )
    return create_ejecucion(db, data)


def crear_ejecucion_paso_en_db(db, ejecucion_id, paso_id):
    ep = EjecucionPaso(
        ejecucion_id=ejecucion_id,
        paso_id=paso_id,
        resultado="pendiente",
        valor_obtenido="",
    )
    db.add(ep)
    db.commit()
    db.refresh(ep)
    return ep


# ============================================================
# TESTS GET
# ============================================================

def test_get_ejecucion_paso_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, caso.id)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    ep = crear_ejecucion_paso_en_db(db, ejec.id, paso.id)

    resultado = get_ejecucion_paso(db, ep.id)
    assert resultado.id == ep.id
    assert resultado.ejecucion_id == ejec.id
    assert resultado.paso_id == paso.id


def test_get_ejecucion_paso_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_ejecucion_paso(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Ejecución de paso no encontrada"


# ============================================================
# TESTS LISTAR
# ============================================================

def test_get_ejecuciones_paso_por_ejecucion(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso1 = crear_paso_en_db(db, caso.id, orden=1)
    paso2 = crear_paso_en_db(db, caso.id, orden=2)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    crear_ejecucion_paso_en_db(db, ejec.id, paso1.id)
    crear_ejecucion_paso_en_db(db, ejec.id, paso2.id)

    lista = get_ejecuciones_paso_por_ejecucion(db, ejec.id)
    assert len(lista) == 2


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_ejecucion_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, caso.id)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    data = EjecucionPasoCreate(
        ejecucion_id=ejec.id,
        paso_id=paso.id,
        resultado="pendiente",
        valor_obtenido=""
    )

    ep = create_ejecucion_paso(db, data)

    assert ep.id is not None
    assert ep.ejecucion_id == ejec.id
    assert ep.paso_id == paso.id
    assert ep.resultado == "pendiente"


def test_create_ejecucion_paso_ejecucion_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, caso.id)

    data = EjecucionPasoCreate(
        ejecucion_id=9999,
        paso_id=paso.id,
        resultado="pendiente",
        valor_obtenido=""
    )

    with pytest.raises(HTTPException) as exc:
        create_ejecucion_paso(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Ejecución no encontrada"


def test_create_ejecucion_paso_paso_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    data = EjecucionPasoCreate(
        ejecucion_id=ejec.id,
        paso_id=9999,
        resultado="pendiente",
        valor_obtenido=""
    )

    with pytest.raises(HTTPException) as exc:
        create_ejecucion_paso(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Paso no encontrado"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_ejecucion_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, caso.id)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    ep = crear_ejecucion_paso_en_db(db, ejec.id, paso.id)

    data = EjecucionPasoUpdate(
        resultado="ok",
        valor_obtenido="Respuesta correcta"
    )

    actualizado = update_ejecucion_paso(db, ep.id, data)

    assert actualizado.resultado == "ok"
    assert actualizado.valor_obtenido == "Respuesta correcta"


def test_update_ejecucion_paso_inexistente(db):
    data = EjecucionPasoUpdate(resultado="ok")

    with pytest.raises(HTTPException) as exc:
        update_ejecucion_paso(db, 9999, data)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_ejecucion_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    caso = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, caso.id)
    usuario = crear_usuario_en_db(db)
    ejec = crear_ejecucion_en_db(db, caso.id, usuario.id)

    ep = crear_ejecucion_paso_en_db(db, ejec.id, paso.id)

    delete_ejecucion_paso(db, ep.id)

    with pytest.raises(HTTPException):
        get_ejecucion_paso(db, ep.id)


def test_delete_ejecucion_paso_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_ejecucion_paso(db, 9999)

    assert exc.value.status_code == 404
