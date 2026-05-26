"""
Tests para services/objeto_parametro.py

Cubre:
- get_objeto_parametro
- get_objetos_parametro_por_paso
- get_objetos_parametro_por_api
- create_objeto_parametro
- update_objeto_parametro
- delete_objeto_parametro

Validando:
- FK a Paso
- FK a API
- Manejo de errores 404
"""

import pytest
from fastapi import HTTPException

from services.objeto_parametro import (
    get_objeto_parametro,
    get_objetos_parametro_por_paso,
    get_objetos_parametro_por_api,
    create_objeto_parametro,
    update_objeto_parametro,
    delete_objeto_parametro,
)

from services.proyecto import create_proyecto
    # ...
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from services.paso import create_paso

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.paso import PasoCreate
from schemas.objeto_parametro import ObjetoParametroCreate, ObjetoParametroUpdate

from models.objeto_parametro import ObjetoParametro
from models.my_api import Api


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
    return create_paso(
        db,
        PasoCreate(
            caso_id=caso_id,
            orden=orden,
            descripcion=descripcion
        )
    )


# 🔧 FIX: API correcta usando endpoint (NO url)
def crear_api_en_db(db, nombre="API Test"):
    api = Api(nombre=nombre, metodo="GET", endpoint="/test")
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


def crear_objeto_parametro_en_db(db, paso_id, api_id=None, tipo="body", nombre="param", entrada="x", esperado="y"):
    obj = ObjetoParametro(
        paso_id=paso_id,
        api_id=api_id,
        tipo=tipo,
        nombre=nombre,
        valor_entrada=entrada,
        valor_esperado=esperado
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ============================================================
# TESTS GET
# ============================================================

def test_get_objeto_parametro_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    obj = crear_objeto_parametro_en_db(db, paso.id)

    resultado = get_objeto_parametro(db, obj.id)
    assert resultado.id == obj.id
    assert resultado.nombre == "param"


def test_get_objeto_parametro_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_objeto_parametro(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Objeto parámetro no encontrado"


def test_get_objetos_parametro_por_paso(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)

    crear_objeto_parametro_en_db(db, paso.id, nombre="A")
    crear_objeto_parametro_en_db(db, paso.id, nombre="B")

    objs = get_objetos_parametro_por_paso(db, paso.id)
    assert len(objs) == 2
    assert {o.nombre for o in objs} == {"A", "B"}


def test_get_objetos_parametro_por_api(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    api = crear_api_en_db(db)

    crear_objeto_parametro_en_db(db, paso.id, api.id, nombre="A")
    crear_objeto_parametro_en_db(db, paso.id, api.id, nombre="B")

    objs = get_objetos_parametro_por_api(db, api.id)
    assert len(objs) == 2
    assert {o.nombre for o in objs} == {"A", "B"}


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_objeto_parametro(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    api = crear_api_en_db(db)

    data = ObjetoParametroCreate(
        paso_id=paso.id,
        api_id=api.id,
        tipo="body",
        nombre="token",
        valor_entrada="123",
        valor_esperado="OK"
    )

    obj = create_objeto_parametro(db, data)

    assert obj.id is not None
    assert obj.paso_id == paso.id
    assert obj.api_id == api.id
    assert obj.nombre == "token"


def test_create_objeto_parametro_paso_inexistente(db):
    data = ObjetoParametroCreate(
        paso_id=9999,
        api_id=None,
        tipo="body",
        nombre="x"
    )

    with pytest.raises(HTTPException) as exc:
        create_objeto_parametro(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Paso no encontrado"


def test_create_objeto_parametro_api_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)

    data = ObjetoParametroCreate(
        paso_id=paso.id,
        api_id=9999,
        tipo="body",
        nombre="x"
    )

    with pytest.raises(HTTPException) as exc:
        create_objeto_parametro(db, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "API no encontrada"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_objeto_parametro(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    api = crear_api_en_db(db)
    obj = crear_objeto_parametro_en_db(db, paso.id, api.id)

    data = ObjetoParametroUpdate(
        nombre="nuevo",
        valor_entrada="in",
        valor_esperado="out"
    )

    actualizado = update_objeto_parametro(db, obj.id, data)

    assert actualizado.nombre == "nuevo"
    assert actualizado.valor_entrada == "in"
    assert actualizado.valor_esperado == "out"


def test_update_objeto_parametro_cambiar_paso_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    obj = crear_objeto_parametro_en_db(db, paso.id)

    data = ObjetoParametroUpdate(paso_id=9999)

    with pytest.raises(HTTPException) as exc:
        update_objeto_parametro(db, obj.id, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Paso no encontrado"


def test_update_objeto_parametro_cambiar_api_inexistente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    obj = crear_objeto_parametro_en_db(db, paso.id)

    data = ObjetoParametroUpdate(api_id=9999)

    with pytest.raises(HTTPException) as exc:
        update_objeto_parametro(db, obj.id, data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "API no encontrada"


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_objeto_parametro(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    obj = crear_objeto_parametro_en_db(db, paso.id)

    delete_objeto_parametro(db, obj.id)

    with pytest.raises(HTTPException):
        get_objeto_parametro(db, obj.id)


def test_delete_objeto_parametro_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_objeto_parametro(db, 9999)

    assert exc.value.status_code == 404
