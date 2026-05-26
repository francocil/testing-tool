from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.rol import (
    get_roles,
    get_rol,
    create_rol,
    update_rol,
    delete_rol,
)
from schemas.rol import RolCreate, RolUpdate, RolResponse

from core.permissions import require_permission

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "/",
    response_model=list[RolResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_rol_ver"))]
)
def listar_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get(
    "/{rol_id}",
    response_model=RolResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_rol_ver"))]
)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    return get_rol(db, rol_id)


@router.post(
    "/",
    response_model=RolResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_rol_crear"))]
)
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return create_rol(db, data)


@router.put(
    "/{rol_id}",
    response_model=RolResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_rol_editar"))]
)
def actualizar_rol(rol_id: int, data: RolUpdate, db: Session = Depends(get_db)):
    return update_rol(db, rol_id, data)


@router.delete(
    "/{rol_id}",
    status_code=204,
    dependencies=[Depends(require_permission("seguridad_rol_eliminar"))]
)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    delete_rol(db, rol_id)
    return Response(status_code=204)
