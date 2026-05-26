from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from models.area import Area

from services.area import (
    get_areas,
    get_area,
    create_area,
    update_area,
    delete_area,
)

from schemas.area import (
    AreaCreate,
    AreaUpdate,
    AreaResponse,
)

# 🔐 Sistema de permisos institucional
from core.permissions import require_permission, require_any_permission

router = APIRouter(prefix="/areas", tags=["Áreas"])


# ============================================================
#  LISTAR ÁREAS
# ------------------------------------------------------------
# Permisos válidos:
#   - ver_areas
#   - ver_organigrama
# ============================================================
@router.get(
    "/",
    response_model=list[AreaResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_areas", "ver_organigrama"))]
)
def listar_areas(
    direccion_id: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Lista áreas. Si se envía direccion_id, filtra por dirección.
    """
    query = db.query(Area)

    if direccion_id is not None:
        query = query.filter(Area.direccion_id == direccion_id)

    return query.all()


# ============================================================
#  OBTENER ÁREA POR ID
# ------------------------------------------------------------
# Permisos válidos:
#   - ver_areas
#   - ver_organigrama
# ============================================================
@router.get(
    "/{area_id}",
    response_model=AreaResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_any_permission("ver_areas", "ver_organigrama"))]
)
def obtener_area_endpoint(area_id: int, db: Session = Depends(get_db)):
    return get_area(db, area_id)


# ============================================================
#  CREAR ÁREA
# ------------------------------------------------------------
# Permisos válidos:
#   - crear_area
# ============================================================
@router.post(
    "/",
    response_model=AreaResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_area"))]
)
def crear_area_endpoint(data: AreaCreate, db: Session = Depends(get_db)):
    return create_area(db, data)


# ============================================================
#  ACTUALIZAR ÁREA
# ------------------------------------------------------------
# Permisos válidos:
#   - editar_area
# ============================================================
@router.put(
    "/{area_id}",
    response_model=AreaResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_area"))]
)
def actualizar_area_endpoint(
    area_id: int,
    data: AreaUpdate,
    db: Session = Depends(get_db),
):
    return update_area(db, area_id, data)


# ============================================================
#  ELIMINAR ÁREA
# ------------------------------------------------------------
# Permisos válidos:
#   - eliminar_area
# ============================================================
@router.delete(
    "/{area_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_area"))]
)
def eliminar_area_endpoint(area_id: int, db: Session = Depends(get_db)):
    delete_area(db, area_id)
