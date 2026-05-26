from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.reparticion import (
    get_reparticiones,
    get_reparticion,
    create_reparticion,
    update_reparticion,
    delete_reparticion,
)
from schemas.reparticion import (
    ReparticionCreate,
    ReparticionUpdate,
    ReparticionResponse,
)

# 🔐 Sistema de permisos institucional
from core.permissions import require_permission, require_any_permission

router = APIRouter(prefix="/reparticiones", tags=["Reparticiones"])


# ============================================================
#  LISTAR REPARTICIONES
# ------------------------------------------------------------
@router.get(
    "/",
    response_model=list[ReparticionResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_reparticiones", "ver_organigrama"))]
)
def listar_reparticiones(db: Session = Depends(get_db)):
    return get_reparticiones(db)


# ============================================================
#  OBTENER REPARTICIÓN POR ID
# ------------------------------------------------------------
@router.get(
    "/{reparticion_id}",
    response_model=ReparticionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_reparticiones", "ver_organigrama"))]
)
def obtener_reparticion_endpoint(reparticion_id: int, db: Session = Depends(get_db)):
    return get_reparticion(db, reparticion_id)


# ============================================================
#  CREAR REPARTICIÓN
# ------------------------------------------------------------
@router.post(
    "/",
    response_model=ReparticionResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_reparticion"))]
)
def crear_reparticion_endpoint(data: ReparticionCreate, db: Session = Depends(get_db)):
    return create_reparticion(db, data)


# ============================================================
#  ACTUALIZAR REPARTICIÓN
# ------------------------------------------------------------
@router.put(
    "/{reparticion_id}",
    response_model=ReparticionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_reparticion"))]
)
def actualizar_reparticion_endpoint(
    reparticion_id: int,
    data: ReparticionUpdate,
    db: Session = Depends(get_db),
):
    return update_reparticion(db, reparticion_id, data)


# ============================================================
#  ELIMINAR REPARTICIÓN
# ------------------------------------------------------------
@router.delete(
    "/{reparticion_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_reparticion"))]
)
def eliminar_reparticion_endpoint(reparticion_id: int, db: Session = Depends(get_db)):
    delete_reparticion(db, reparticion_id)
