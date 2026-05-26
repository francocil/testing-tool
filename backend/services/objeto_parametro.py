from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.objeto_parametro import ObjetoParametro
from models.paso import Paso
from models.my_api import Api

from schemas.objeto_parametro import (
    ObjetoParametroCreate,
    ObjetoParametroUpdate
)

from jsonpath_ng import parse as jsonpath_parse
import json
import re


# ============================================================
#  CONSTANTES DE VALIDACIÓN
# ============================================================

TIPOS_VALIDOS = {
    "entrada",        # parámetro de entrada (body/query/header/path)
    "esperado",       # valor esperado para asserts
    "header",         # header HTTP
    "query",          # query param
    "path",           # path param
    "variable",       # variable de contexto
    "contexto",       # lectura desde contexto
    "body",           # body completo o parcial
    "jsonpath",       # expresión JSONPath
}


# ============================================================
#  HELPERS DE VALIDACIÓN
# ============================================================

def _validar_tipo(tipo: str | None):
    if tipo is None:
        return
    if tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de parámetro inválido: {tipo}. Valores permitidos: {', '.join(sorted(TIPOS_VALIDOS))}"
        )


def _validar_nombre(nombre: str | None):
    if not nombre:
        raise HTTPException(status_code=400, detail="El nombre del parámetro es obligatorio")
    if len(nombre) > 100:
        raise HTTPException(status_code=400, detail="El nombre del parámetro no puede superar 100 caracteres")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", nombre):
        raise HTTPException(
            status_code=400,
            detail="El nombre del parámetro debe ser un identificador válido (letras, números, guiones bajos, sin espacios)"
        )


def _validar_json_string(valor: str | None, nombre: str):
    if valor is None:
        return
    try:
        json.loads(valor)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"{nombre} debe ser un JSON válido (string serializado)"
        )


def _validar_jsonpath(expr: str | None, nombre: str):
    if expr is None:
        return
    try:
        jsonpath_parse(expr)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"{nombre} debe ser una expresión JSONPath válida"
        )


def _validar_coherencia_tipo_valores(tipo: str, valor_entrada: str | None, valor_esperado: str | None):
    # tipo esperado → valor_esperado obligatorio
    if tipo == "esperado" and not valor_esperado:
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'esperado', el campo 'valor_esperado' es obligatorio"
        )

    # tipo body → valor_entrada debe ser JSON
    if tipo == "body" and not valor_entrada:
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'body', el campo 'valor_entrada' es obligatorio y debe ser JSON"
        )

    # tipo jsonpath → valor_esperado debe ser JSONPath
    if tipo == "jsonpath" and not valor_esperado:
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'jsonpath', el campo 'valor_esperado' es obligatorio y debe ser JSONPath"
        )


def _validar_paso_y_api(db: Session, paso_id: int | None, api_id: int | None):
    paso = None
    api = None

    if paso_id is not None:
        paso = db.query(Paso).filter(Paso.id == paso_id).first()
        if not paso:
            raise HTTPException(status_code=404, detail="Paso no encontrado")

    if api_id is not None:
        api = db.query(Api).filter(Api.id == api_id).first()
        if not api:
            raise HTTPException(status_code=404, detail="API no encontrada")

    # Coherencia: si el paso tiene API asociada, api_id debe coincidir (si se envía)
    if paso and paso.api_id is not None and api_id is not None and api_id != paso.api_id:
        raise HTTPException(
            status_code=400,
            detail="El parámetro está asociado a un paso cuya API no coincide con api_id"
        )

    return paso, api


def _validar_no_duplicado(db: Session, paso_id: int | None, api_id: int | None, nombre: str, objeto_id: int | None = None):
    query = db.query(ObjetoParametro).filter(ObjetoParametro.nombre == nombre)

    if paso_id is not None:
        query = query.filter(ObjetoParametro.paso_id == paso_id)
    if api_id is not None:
        query = query.filter(ObjetoParametro.api_id == api_id)
    if objeto_id is not None:
        query = query.filter(ObjetoParametro.id != objeto_id)

    existente = query.first()
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un parámetro con ese nombre para este paso/API"
        )


def _validar_no_usado_en_ejecuciones(db: Session, objeto_parametro_id: int):
    # Hook para futuro: si luego agregás relación con ejecuciones,
    # acá bloqueás borrado/edición. Hoy no hay relación directa.
    return


# ============================================================
#  GETTERS
# ============================================================

def get_objeto_parametro(db: Session, objeto_parametro_id: int) -> ObjetoParametro:
    objeto = (
        db.query(ObjetoParametro)
        .options(
            joinedload(ObjetoParametro.paso),
            joinedload(ObjetoParametro.api),
        )
        .filter(ObjetoParametro.id == objeto_parametro_id)
        .first()
    )

    if not objeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objeto parámetro no encontrado"
        )

    return objeto


def get_objetos_parametro_por_paso(db: Session, paso_id: int) -> list[ObjetoParametro]:
    return (
        db.query(ObjetoParametro)
        .options(
            joinedload(ObjetoParametro.paso),
            joinedload(ObjetoParametro.api),
        )
        .filter(ObjetoParametro.paso_id == paso_id)
        .all()
    )


def get_objetos_parametro_por_api(db: Session, api_id: int) -> list[ObjetoParametro]:
    return (
        db.query(ObjetoParametro)
        .options(
            joinedload(ObjetoParametro.paso),
            joinedload(ObjetoParametro.api),
        )
        .filter(ObjetoParametro.api_id == api_id)
        .all()
    )


# ============================================================
#  CREAR
# ============================================================

def create_objeto_parametro(db: Session, data: ObjetoParametroCreate) -> ObjetoParametro:
    _validar_tipo(data.tipo)
    _validar_nombre(data.nombre)

    # Validar coherencia paso / api
    _validar_paso_y_api(db, data.paso_id, data.api_id)

    # Validar duplicado
    _validar_no_duplicado(db, data.paso_id, data.api_id, data.nombre)

    # Validar valores según tipo
    _validar_coherencia_tipo_valores(data.tipo, data.valor_entrada, data.valor_esperado)

    # Validar JSON y JSONPath cuando corresponda
    if data.tipo in {"body"} and data.valor_entrada:
        _validar_json_string(data.valor_entrada, "valor_entrada")

    if data.tipo in {"jsonpath", "esperado"} and data.valor_esperado:
        _validar_jsonpath(data.valor_esperado, "valor_esperado")

    nuevo = ObjetoParametro(
        paso_id=data.paso_id,
        api_id=data.api_id,
        tipo=data.tipo,
        nombre=data.nombre,
        valor_entrada=data.valor_entrada,
        valor_esperado=data.valor_esperado
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ============================================================
#  ACTUALIZAR
# ============================================================

def update_objeto_parametro(db: Session, objeto_parametro_id: int, data: ObjetoParametroUpdate) -> ObjetoParametro:
    objeto = get_objeto_parametro(db, objeto_parametro_id)

    _validar_no_usado_en_ejecuciones(db, objeto_parametro_id)

    # Determinar valores finales para validar coherencia
    paso_id_final = data.paso_id if data.paso_id is not None else objeto.paso_id
    api_id_final = data.api_id if data.api_id is not None else objeto.api_id
    tipo_final = data.tipo if data.tipo is not None else objeto.tipo
    nombre_final = data.nombre if data.nombre is not None else objeto.nombre
    valor_entrada_final = data.valor_entrada if data.valor_entrada is not None else objeto.valor_entrada
    valor_esperado_final = data.valor_esperado if data.valor_esperado is not None else objeto.valor_esperado

    _validar_tipo(tipo_final)
    _validar_nombre(nombre_final)
    _validar_paso_y_api(db, paso_id_final, api_id_final)
    _validar_no_duplicado(db, paso_id_final, api_id_final, nombre_final, objeto_id=objeto.id)
    _validar_coherencia_tipo_valores(tipo_final, valor_entrada_final, valor_esperado_final)

    if tipo_final in {"body"} and valor_entrada_final:
        _validar_json_string(valor_entrada_final, "valor_entrada")

    if tipo_final in {"jsonpath", "esperado"} and valor_esperado_final:
        _validar_jsonpath(valor_esperado_final, "valor_esperado")

    # Aplicar cambios
    if data.paso_id is not None:
        objeto.paso_id = data.paso_id

    if data.api_id is not None:
        objeto.api_id = data.api_id

    if data.tipo is not None:
        objeto.tipo = data.tipo

    if data.nombre is not None:
        objeto.nombre = data.nombre

    if data.valor_entrada is not None:
        objeto.valor_entrada = data.valor_entrada

    if data.valor_esperado is not None:
        objeto.valor_esperado = data.valor_esperado

    db.commit()
    db.refresh(objeto)
    return objeto


# ============================================================
#  ELIMINAR
# ============================================================

def delete_objeto_parametro(db: Session, objeto_parametro_id: int) -> None:
    objeto = get_objeto_parametro(db, objeto_parametro_id)

    _validar_no_usado_en_ejecuciones(db, objeto_parametro_id)

    try:
        db.delete(objeto)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el parámetro porque está asociado a otros registros"
        )
