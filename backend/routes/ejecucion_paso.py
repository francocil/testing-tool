from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.ejecucion_paso import (
    get_ejecucion_paso,
    list_ejecucion_pasos,
    update_ejecucion_paso,
    registrar_paso_manual,
)
from schemas.ejecucion_paso import (
    EjecucionPasoUpdate,
    EjecucionPaso,
)

from core.permissions import require_permission


router = APIRouter(prefix="/ejecuciones-pasos", tags=["EjecucionPaso"])


# ============================================================
# LISTAR PASOS DE UNA EJECUCIÓN
# ============================================================
@router.get(
    "/ejecucion/{ejecucion_id}",
    response_model=list[EjecucionPaso],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ejecucion_ver_todos"))]
)
def listar_ejecuciones_paso_por_ejecucion(ejecucion_id: int, db: Session = Depends(get_db)):
    return list_ejecucion_pasos(db, ejecucion_id)


# ============================================================
# OBTENER PASO DE EJECUCIÓN POR ID
# ============================================================
@router.get(
    "/{ejecucion_paso_id}",
    response_model=EjecucionPaso,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ejecucion_ver_todos"))]
)
def obtener_ejecucion_paso_endpoint(ejecucion_paso_id: int, db: Session = Depends(get_db)):
    return get_ejecucion_paso(db, ejecucion_paso_id)


# ============================================================
# ACTUALIZAR PASO DE EJECUCIÓN
# ============================================================
@router.put(
    "/{ejecucion_paso_id}",
    response_model=EjecucionPaso,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ejecucion_editar"))]
)
def actualizar_ejecucion_paso_endpoint(ejecucion_paso_id: int, data: EjecucionPasoUpdate, db: Session = Depends(get_db)):
    return update_ejecucion_paso(db, ejecucion_paso_id, data)


# ============================================================
# REGISTRAR PASO MANUAL
# ============================================================
@router.post(
    "/manual/{ejecucion_id}/{paso_id}",
    response_model=EjecucionPaso,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ejecucion_registrar_manual"))]
)
def registrar_paso_manual_endpoint(
    ejecucion_id: int,
    paso_id: int,
    estado: str,
    resultado_texto: str,
    db: Session = Depends(get_db)
):
    return registrar_paso_manual(
        db=db,
        ejecucion_id=ejecucion_id,
        paso_id=paso_id,
        estado=estado,
        resultado_texto=resultado_texto
    )
