from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import json

from models.ejecucion_paso import EjecucionPaso
from models.ejecucion import Ejecucion
from models.paso import Paso
from schemas.ejecucion_paso import EjecucionPasoUpdate


# ============================================================
#  Helpers
# ============================================================

def _http_400(msg: str):
    return HTTPException(status_code=400, detail=msg)


def _get_ejecucion_or_404(db: Session, ejecucion_id: int) -> Ejecucion:
    ejec = db.query(Ejecucion).filter(Ejecucion.id == ejecucion_id).first()
    if not ejec:
        raise HTTPException(404, "Ejecución no encontrada")
    return ejec


def _get_ejecucion_paso_or_404(db: Session, ejecucion_paso_id: int) -> EjecucionPaso:
    ep = db.query(EjecucionPaso).filter(EjecucionPaso.id == ejecucion_paso_id).first()
    if not ep:
        raise HTTPException(404, "Ejecución de paso no encontrada")
    return ep


def _validate_json(value, field_name):
    if value is None:
        return
    if not isinstance(value, (dict, list)):
        raise _http_400(f"{field_name} debe ser JSON válido")


def _validate_tipo_resultado(value: str | None):
    if value is None:
        return
    if value not in {"ok", "fallo_assert", "error_tecnico", "simulado", "manual_ok", "manual_error"}:
        raise _http_400(f"tipo_resultado inválido: {value}")


# ============================================================
#  Obtener EjecucionPaso
# ============================================================

def get_ejecucion_paso(db: Session, ejecucion_paso_id: int) -> EjecucionPaso:
    return _get_ejecucion_paso_or_404(db, ejecucion_paso_id)


# ============================================================
#  Listar pasos de una ejecución
# ============================================================

def list_ejecucion_pasos(db: Session, ejecucion_id: int):
    _get_ejecucion_or_404(db, ejecucion_id)

    return (
        db.query(EjecucionPaso)
        .join(Paso, Paso.id == EjecucionPaso.paso_id)
        .filter(EjecucionPaso.ejecucion_id == ejecucion_id)
        .order_by(Paso.orden.asc())
        .all()
    )


# ============================================================
#  Actualizar EjecucionPaso
# ============================================================

def update_ejecucion_paso(db: Session, ejecucion_paso_id: int, data: EjecucionPasoUpdate) -> EjecucionPaso:
    ep = _get_ejecucion_paso_or_404(db, ejecucion_paso_id)
    ejec = _get_ejecucion_or_404(db, ep.ejecucion_id)

    # No permitir actualizar pasos de ejecuciones finalizadas
    if ejec.estado in {"finalizado", "cancelado"}:
        raise _http_400("No se puede modificar pasos de una ejecución finalizada o cancelada")

    # Validaciones
    _validate_tipo_resultado(data.tipo_resultado)
    _validate_json(data.request_json, "request_json")
    _validate_json(data.response_json, "response_json")
    _validate_json(data.asserts_json, "asserts_json")
    _validate_json(data.errores_json, "errores_json")

    if data.duracion_ms is not None and data.duracion_ms < 0:
        raise _http_400("duracion_ms no puede ser negativa")

    # Aplicar cambios
    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(ep, campo, valor)

    db.commit()
    db.refresh(ep)
    return ep


# ============================================================
#  Registrar paso manual (delegado al motor)
# ============================================================

def registrar_paso_manual(
    db: Session,
    ejecucion_id: int,
    paso_id: int,
    estado: str,
    resultado_texto: str
) -> EjecucionPaso:
    from services.motor_ejecucion import registrar_paso_manual as motor_registrar

    return motor_registrar(
        db=db,
        ejecucion_id=ejecucion_id,
        paso_id=paso_id,
        estado=estado,
        resultado_texto=resultado_texto,
    )
