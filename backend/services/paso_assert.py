from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jsonpath_ng import parse as jsonpath_parse
import re

from models.paso_assert import PasoAssert
from models.paso import Paso
from schemas.paso_assert import PasoAssertCreate, PasoAssertUpdate


# ------------------------------------------------------------
#  Tipos permitidos
# ------------------------------------------------------------
ALLOWED_TIPOS = {
    "status_code",
    "jsonpath",
    "header",
    "body_contains",
    "regex",
    "length",
}

# ------------------------------------------------------------
#  Operadores permitidos (nuevos)
# ------------------------------------------------------------
ALLOWED_OPERADORES = {
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "gt",
    "gte",
    "lt",
    "lte",
    "matches_regex",
    "len_equals",
    "len_gt",
    "len_lt",
}

# ------------------------------------------------------------
#  Operadores legacy (compatibilidad)
# ------------------------------------------------------------
LEGACY_OPERADORES = {
    "==",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "contains",
    "not_contains",
}


# ============================================================
#  Helpers
# ============================================================

def _http_400(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def _validate_order_unique(db: Session, paso_id: int, orden: int, exclude_id: int | None = None):
    query = db.query(PasoAssert).filter(
        PasoAssert.paso_id == paso_id,
        PasoAssert.orden == orden
    )
    if exclude_id:
        query = query.filter(PasoAssert.id != exclude_id)

    if query.first():
        raise _http_400(f"Ya existe un assert con orden {orden} en este paso")


def _validate_paso_tipo(paso: Paso):
    if paso.tipo not in {"automatico", "mixto", "simulado"}:
        raise _http_400("Los asserts solo pueden crearse en pasos automáticos, mixtos o simulados")


def _validate_assert_fields(tipo: str, operador: str,
                            expresion: str | None,
                            valor_esperado: str | None) -> None:

    # tipo válido
    if tipo not in ALLOWED_TIPOS:
        raise _http_400(f"Tipo de assert inválido: {tipo}")

    # operador válido
    if operador not in ALLOWED_OPERADORES and operador not in LEGACY_OPERADORES:
        raise _http_400(f"Operador de assert inválido: {operador}")

    # reglas por tipo
    if tipo in {"jsonpath", "header"} and not expresion:
        raise _http_400("El campo 'expresion' es obligatorio para este tipo de assert")

    if tipo == "regex" and not valor_esperado:
        raise _http_400("El campo 'valor_esperado' es obligatorio para asserts de tipo regex")

    # operadores numéricos
    numeric_ops = {"gt", "gte", "lt", "lte", ">", "<", ">=", "<="}
    if operador in numeric_ops:
        if valor_esperado is None:
            raise _http_400("El campo 'valor_esperado' es obligatorio para comparaciones numéricas")
        try:
            float(valor_esperado)
        except Exception:
            raise _http_400("El campo 'valor_esperado' debe ser numérico para este operador")

    # operadores de longitud
    length_ops = {"len_equals", "len_gt", "len_lt"}
    if operador in length_ops:
        if valor_esperado is None:
            raise _http_400("El campo 'valor_esperado' es obligatorio para operadores de longitud")
        try:
            int(valor_esperado)
        except Exception:
            raise _http_400("El campo 'valor_esperado' debe ser entero para operadores de longitud")

    # validar JSONPath si corresponde
    if tipo == "jsonpath" and expresion:
        try:
            jsonpath_parse(expresion)
        except Exception as e:
            raise _http_400(f"Expresión JSONPath inválida: {str(e)}")

    # validar regex si corresponde
    if operador == "matches_regex" and valor_esperado:
        try:
            re.compile(valor_esperado)
        except Exception as e:
            raise _http_400(f"Expresión regex inválida: {str(e)}")


def _validate_paso_assert_instance(pa: PasoAssert) -> None:
    _validate_assert_fields(
        tipo=pa.tipo,
        operador=pa.operador,
        expresion=pa.expresion,
        valor_esperado=pa.valor_esperado,
    )


# ============================================================
#  CRUD
# ============================================================

def list_asserts_by_paso(db: Session, paso_id: int):
    paso = db.query(Paso).filter(Paso.id == paso_id).first()
    if not paso:
        raise HTTPException(status_code=404, detail="Paso no encontrado")

    return (
        db.query(PasoAssert)
        .filter(PasoAssert.paso_id == paso_id)
        .order_by(PasoAssert.orden.asc())
        .all()
    )


def create_assert(db: Session, paso_id: int, data: PasoAssertCreate):
    paso = db.query(Paso).filter(Paso.id == paso_id).first()
    if not paso:
        raise HTTPException(status_code=404, detail="Paso no encontrado")

    _validate_paso_tipo(paso)
    _validate_order_unique(db, paso_id, data.orden)

    _validate_assert_fields(
        tipo=data.tipo,
        operador=data.operador,
        expresion=data.expresion,
        valor_esperado=data.valor_esperado,
    )

    nuevo = PasoAssert(
        paso_id=paso_id,
        tipo=data.tipo,
        expresion=data.expresion,
        operador=data.operador,
        valor_esperado=data.valor_esperado,
        mensaje_error=data.mensaje_error,
        orden=data.orden,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_assert(db: Session, assert_id: int, data: PasoAssertUpdate):
    pa = db.query(PasoAssert).filter(PasoAssert.id == assert_id).first()
    if not pa:
        raise HTTPException(status_code=404, detail="Assert no encontrado")

    if data.orden is not None:
        _validate_order_unique(db, pa.paso_id, data.orden, exclude_id=pa.id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pa, field, value)

    _validate_paso_assert_instance(pa)

    db.commit()
    db.refresh(pa)
    return pa


def delete_assert(db: Session, assert_id: int):
    pa = db.query(PasoAssert).filter(PasoAssert.id == assert_id).first()
    if not pa:
        raise HTTPException(status_code=404, detail="Assert no encontrado")

    db.delete(pa)
    db.commit()
    return {"detail": "Assert eliminado correctamente"}
