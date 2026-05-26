from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.caso_prueba_version import (
    get_caso_prueba_versiones,
    get_caso_prueba_version,
    create_caso_prueba_version,
    update_caso_prueba_version,
    delete_caso_prueba_version,
)
from schemas.caso_prueba_version import (
    CasoPruebaVersionCreate,
    CasoPruebaVersionUpdate,
    CasoPruebaVersionResponse,
)

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


router = APIRouter(prefix="/casos-prueba-versiones", tags=["CasoPruebaVersiones"])


# ============================================================
#  LISTAR TODAS LAS VERSIONES
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_casos"
# ============================================================
@router.get(
    "/",
    response_model=list[CasoPruebaVersionResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_casos"))]
)
def listar_versiones(db: Session = Depends(get_db)):
    return get_caso_prueba_versiones(db)


# ============================================================
#  OBTENER VERSIÓN POR ID
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_casos"
# ============================================================
@router.get(
    "/{version_id}",
    response_model=CasoPruebaVersionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_casos"))]
)
def obtener_version(version_id: int, db: Session = Depends(get_db)):
    return get_caso_prueba_version(db, version_id)


# ============================================================
#  CREAR VERSIÓN
# ------------------------------------------------------------
#  Permiso requerido:
#     - "versionar_casos"
# ============================================================
@router.post(
    "/",
    response_model=CasoPruebaVersionResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("versionar_casos"))]
)
def crear_version(data: CasoPruebaVersionCreate, db: Session = Depends(get_db)):
    return create_caso_prueba_version(db, data)


# ============================================================
#  ACTUALIZAR VERSIÓN
# ------------------------------------------------------------
#  Permiso requerido:
#     - "versionar_casos"
# ============================================================
@router.put(
    "/{version_id}",
    response_model=CasoPruebaVersionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("versionar_casos"))]
)
def actualizar_version(version_id: int, data: CasoPruebaVersionUpdate, db: Session = Depends(get_db)):
    return update_caso_prueba_version(db, version_id, data)


# ============================================================
#  ELIMINAR VERSIÓN
# ------------------------------------------------------------
#  Permiso requerido:
#     - "versionar_casos"
# ============================================================
@router.delete(
    "/{version_id}",
    status_code=204,
    dependencies=[Depends(require_permission("versionar_casos"))]
)
def eliminar_version(version_id: int, db: Session = Depends(get_db)):
    delete_caso_prueba_version(db, version_id)
    return Response(status_code=204)
