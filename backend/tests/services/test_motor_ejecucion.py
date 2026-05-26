"""
Tests del motor de ejecución (services/motor_ejecucion.py)

Cubre:
- Inicialización de pasos
- Ejecución automática real (mockeada)
- Ejecución manual
- Ejecución completa en modo automático
- Ejecución completa en modo mixto
"""

import pytest
from unittest.mock import patch

from services.motor_ejecucion import (
    ejecutar_ejecucion,
    ejecutar_siguiente_paso,
    registrar_paso_manual
)

from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from services.usuario import create_usuario
from services.paso import create_paso
from services.my_api import create_api
from services.objeto_parametro import create_objeto_parametro
from services.ejecucion import create_ejecucion

from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.usuario import UsuarioCreate
from schemas.paso import PasoCreate
from schemas.my_api import ApiCreate
from schemas.objeto_parametro import ObjetoParametroCreate
from schemas.ejecucion import EjecucionCreate


# ============================================================
# HELPERS
# ============================================================

def crear_entorno_minimo(db):
    """
    Crea un entorno real completo:
    - Proyecto
    - Módulo
    - Caso
    - Usuario
    - Paso automático (API válida)
    - Paso manual
    - Parámetro real
    - Ejecución real
    """

    # Proyecto
    proyecto = create_proyecto(
        db,
        ProyectoCreate(
            nombre="Proyecto Test",
            objetivo_general="Obj",
            contexto="Ctx"
        )
    )

    # Módulo
    modulo = create_modulo(
        db,
        ModuloCreate(
            proyecto_id=proyecto.id,
            nombre="Modulo Test",
            tipo_interfaz="API",
            tipo_gui="web",
            descripcion="desc"
        )
    )

    # Caso
    caso = create_caso_prueba(
        db,
        CasoPruebaCreate(
            modulo_id=modulo.id,
            nombre="Caso Test",
            objetivo="Objetivo",
            porcentaje_aceptacion=80.0
        )
    )

    # Usuario
    usuario = create_usuario(
        db,
        UsuarioCreate(
            nombre="Tester",
            email="tester@test.com",
            password="1234",
            rol_id=1
        )
    )

    # API válida
    api = create_api(
        db,
        ApiCreate(
            nombre="API Test",
            metodo="GET",
            endpoint="https://fake/api"
        )
    )

    # Paso automático
    paso_auto = create_paso(
        db,
        PasoCreate(
            caso_id=caso.id,
            descripcion="Paso automático",
            orden=1
        )
    )

    # Parámetro del paso automático
    create_objeto_parametro(
        db,
        ObjetoParametroCreate(
            paso_id=paso_auto.id,
            api_id=api.id,
            tipo="query",
            nombre="id",
            valor_entrada="123",
            valor_esperado="$.data.id"
        )
    )

    # Paso manual
    paso_manual = create_paso(
        db,
        PasoCreate(
            caso_id=caso.id,
            descripcion="Paso manual",
            orden=2
        )
    )

    # Ejecución
    ejec = create_ejecucion(
        db,
        EjecucionCreate(
            caso_id=caso.id,
            usuario_id=usuario.id,
            modo="automatico",
            resultado_global=None,
            porcentaje_aceptacion=None
        )
    )

    return ejec, paso_auto, paso_manual


# ============================================================
# TESTS
# ============================================================

def test_inicializacion_ejecucion(db):
    ejec, _, _ = crear_entorno_minimo(db)

    ejecutar_siguiente_paso(db, ejec.id)
    db.refresh(ejec)

    assert len(ejec.pasos) == 2


@patch("httpx.Client.request")
def test_ejecucion_automatica_real(mock_request, db):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json = lambda: {"data": {"id": "123"}}
    mock_request.return_value.text = '{"data":{"id":"123"}}'

    ejec, paso_auto, _ = crear_entorno_minimo(db)

    ejecutar_siguiente_paso(db, ejec.id)
    db.refresh(ejec)

    ep = next(ep for ep in ejec.pasos if ep.paso_id == paso_auto.id)

    assert ep.resultado == "ok"
    assert isinstance(ep.valor_obtenido, str)
    assert "request" in ep.valor_obtenido


def test_ejecucion_manual(db):
    ejec, paso_auto, paso_manual = crear_entorno_minimo(db)

    # Ejecutar paso automático primero
    with patch("httpx.Client.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = lambda: {"data": {"id": "123"}}
        mock_request.return_value.text = '{"data":{"id":"123"}}'
        ejecutar_siguiente_paso(db, ejec.id)

    # Registrar manual
    registrar_paso_manual(db, ejec.id, paso_manual.id, "ok", "Todo bien")

    ep_manual = next(ep for ep in ejec.pasos if ep.paso_id == paso_manual.id)

    assert ep_manual.resultado == "ok"
    assert ep_manual.valor_obtenido == "Todo bien"


def test_ejecucion_completa_modo_automatico(db):
    ejec, paso_auto, paso_manual = crear_entorno_minimo(db)

    with patch("httpx.Client.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = lambda: {"data": {"id": "123"}}
        mock_request.return_value.text = '{"data":{"id":"123"}}'

        ejecutar_ejecucion(db, ejec.id)

    db.refresh(ejec)

    assert ejec.estado == "en_progreso"
    assert next(ep for ep in ejec.pasos if ep.paso_id == paso_auto.id).resultado == "ok"
    assert next(ep for ep in ejec.pasos if ep.paso_id == paso_manual.id).resultado == "pendiente"


def test_ejecucion_completa_modo_mixto(db):
    ejec, paso_auto, paso_manual = crear_entorno_minimo(db)

    ejec.modo = "mixto"
    db.commit()

    with patch("httpx.Client.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = lambda: {"data": {"id": "123"}}
        mock_request.return_value.text = '{"data":{"id":"123"}}'

        ejecutar_ejecucion(db, ejec.id)

    db.refresh(ejec)

    assert ejec.estado == "en_progreso"
    assert next(ep for ep in ejec.pasos if ep.paso_id == paso_auto.id).resultado == "ok"
    assert next(ep for ep in ejec.pasos if ep.paso_id == paso_manual.id).resultado == "pendiente"
