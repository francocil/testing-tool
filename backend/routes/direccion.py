from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from models.direccion import Direccion

from services.direccion import (
    get_direcciones,
    get_direccion,
    create_direccion,
    update_direccion,
    delete_direccion,
)

from schemas.direccion import (
    DireccionCreate,
    DireccionUpdate,
    DireccionResponse,
)

# 🔐 Sistema de permisos institucional
from core.permissions import require_permission, require_any_permission

router = APIRouter(prefix="/direcciones", tags=["Direcciones"])


# ============================================================
#  LISTAR DIRECCIONES
# ------------------------------------------------------------
@router.get(
    "/",
    response_model=list[DireccionResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_direcciones", "ver_organigrama"))]
)
def listar_direcciones(
    reparticion_id: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Lista direcciones. Si se envía reparticion_id, filtra por repartición.
    """
    return get_direcciones(db, reparticion_id)
    

# ============================================================
#  OBTENER DIRECCIÓN POR ID
# ------------------------------------------------------------
@router.get(
    "/{direccion_id}",
    response_model=DireccionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_direcciones", "ver_organigrama"))]
)
def obtener_direccion_endpoint(direccion_id: int, db: Session = Depends(get_db)):
    return get_direccion(db, direccion_id)


# ============================================================
#  CREAR DIRECCIÓN
# ------------------------------------------------------------
@router.post(
    "/",
    response_model=DireccionResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_direccion"))]
)
def crear_direccion_endpoint(data: DireccionCreate, db: Session = Depends(get_db)):
    return create_direccion(db, data)


# ============================================================
#  ACTUALIZAR DIRECCIÓN
# ------------------------------------------------------------
@router.put(
    "/{direccion_id}",
    response_model=DireccionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_direccion"))]
)
def actualizar_direccion_endpoint(
    direccion_id: int,
    data: DireccionUpdate,
    db: Session = Depends(get_db),
):
    return update_direccion(db, direccion_id, data)


# ============================================================
#  ELIMINAR DIRECCIÓN
# ------------------------------------------------------------
@router.delete(
    "/{direccion_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_direccion"))]
)
def eliminar_direccion_endpoint(direccion_id: int, db: Session = Depends(get_db)):
    delete_direccion(db, direccion_id)
