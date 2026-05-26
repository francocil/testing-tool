from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from db.session import get_db
from services.auditoria import listar_eventos
from schemas.auditoria import AuditoriaOut

# 🔐 Sistema de permisos institucional
from core.permissions import require_permission

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get(
    "/",
    response_model=List[AuditoriaOut],
    dependencies=[Depends(require_permission("auditoria_ver"))]
)
def obtener_auditoria(
    usuario_id: Optional[int] = Query(None),
    accion: Optional[str] = Query(None),
    fecha_desde: Optional[datetime] = Query(None),
    fecha_hasta: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Consulta de auditoría con filtros opcionales:
    - usuario_id
    - acción (login, logout, refresh, login_failed, etc.)
    - rango de fechas
    - paginación
    """

    Auditoria = listar_eventos.__globals__["Auditoria"]

    query = db.query(Auditoria)

    if usuario_id is not None:
        query = query.filter(Auditoria.usuario_id == usuario_id)

    if accion is not None:
        query = query.filter(Auditoria.accion == accion)

    if fecha_desde is not None:
        query = query.filter(Auditoria.fecha >= fecha_desde)

    if fecha_hasta is not None:
        query = query.filter(Auditoria.fecha <= fecha_hasta)

    query = query.order_by(Auditoria.fecha.desc())

    return query.offset(skip).limit(limit).all()
