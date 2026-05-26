from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.permiso import (
    get_permisos,
    get_permiso,
    create_permiso,
    update_permiso,
    delete_permiso,
)
from schemas.permiso import (
    PermisoCreate,
    PermisoUpdate,
    PermisoResponse,
)

from core.permissions import require_permission

router = APIRouter(prefix="/permisos", tags=["Permisos"])


@router.get(
    "/",
    response_model=list[PermisoResponse],
    dependencies=[Depends(require_permission("seguridad_permiso_ver"))]
)
def listar_permisos(db: Session = Depends(get_db)):
    return get_permisos(db)


@router.get(
    "/{permiso_id}",
    response_model=PermisoResponse,
    dependencies=[Depends(require_permission("seguridad_permiso_ver"))]
)
def obtener_permiso(permiso_id: int, db: Session = Depends(get_db)):
    return get_permiso(db, permiso_id)


@router.post(
    "/",
    response_model=PermisoResponse,
    dependencies=[Depends(require_permission("seguridad_permiso_crear"))]
)
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    return create_permiso(db, data)


@router.put(
    "/{permiso_id}",
    response_model=PermisoResponse,
    dependencies=[Depends(require_permission("seguridad_permiso_editar"))]
)
def actualizar_permiso(permiso_id: int, data: PermisoUpdate, db: Session = Depends(get_db)):
    return update_permiso(db, permiso_id, data)


@router.delete(
    "/{permiso_id}",
    dependencies=[Depends(require_permission("seguridad_permiso_eliminar"))]
)
def eliminar_permiso(permiso_id: int, db: Session = Depends(get_db)):
    delete_permiso(db, permiso_id)
    return {"detail": "Permiso eliminado correctamente"}
