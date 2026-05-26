from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.rol_permiso import (
    get_roles_permisos,
    get_rol_permiso,
    create_rol_permiso,
    update_rol_permiso,
    delete_rol_permiso,
)
from schemas.rol_permiso import (
    RolPermisoCreate,
    RolPermisoUpdate,
    RolPermisoResponse,
)

from core.permissions import require_permission

router = APIRouter(prefix="/roles-permisos", tags=["Roles - Permisos"])


@router.get(
    "/",
    response_model=list[RolPermisoResponse],
    dependencies=[Depends(require_permission("seguridad_rol_permiso_asignar"))]
)
def listar_roles_permisos(db: Session = Depends(get_db)):
    return get_roles_permisos(db)


@router.get(
    "/{rp_id}",
    response_model=RolPermisoResponse,
    dependencies=[Depends(require_permission("seguridad_rol_permiso_asignar"))]
)
def obtener_rol_permiso(rp_id: int, db: Session = Depends(get_db)):
    return get_rol_permiso(db, rp_id)


@router.post(
    "/",
    response_model=RolPermisoResponse,
    dependencies=[Depends(require_permission("seguridad_rol_permiso_asignar"))]
)
def crear_rol_permiso(data: RolPermisoCreate, db: Session = Depends(get_db)):
    return create_rol_permiso(db, data)


@router.put(
    "/{rp_id}",
    response_model=RolPermisoResponse,
    dependencies=[Depends(require_permission("seguridad_rol_permiso_asignar"))]
)
def actualizar_rol_permiso(rp_id: int, data: RolPermisoUpdate, db: Session = Depends(get_db)):
    return update_rol_permiso(db, rp_id, data)


@router.delete(
    "/{rp_id}",
    dependencies=[Depends(require_permission("seguridad_rol_permiso_asignar"))]
)
def eliminar_rol_permiso(rp_id: int, db: Session = Depends(get_db)):
    delete_rol_permiso(db, rp_id)
    return {"detail": "Asignación rol-permiso eliminada correctamente"}
