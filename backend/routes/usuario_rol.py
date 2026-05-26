from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.usuario_rol import (
    get_usuarios_roles,
    get_usuario_rol,
    create_usuario_rol,
    update_usuario_rol,
    delete_usuario_rol,
)
from schemas.usuario_rol import (
    UsuarioRolCreate,
    UsuarioRolUpdate,
    UsuarioRolResponse,
)

from core.permissions import require_permission, require_any_permission

router = APIRouter(prefix="/usuarios-roles", tags=["Usuarios - Roles"])


@router.get(
    "/",
    response_model=list[UsuarioRolResponse],
    dependencies=[Depends(require_permission("seguridad_usuario_rol_asignar"))]
)
def listar_usuarios_roles(db: Session = Depends(get_db)):
    return get_usuarios_roles(db)


@router.get(
    "/{ur_id}",
    response_model=UsuarioRolResponse,
    dependencies=[Depends(require_permission("seguridad_usuario_rol_asignar"))]
)
def obtener_usuario_rol(ur_id: int, db: Session = Depends(get_db)):
    return get_usuario_rol(db, ur_id)


@router.post(
    "/",
    response_model=UsuarioRolResponse,
    dependencies=[Depends(require_permission("seguridad_usuario_rol_asignar"))]
)
def crear_usuario_rol(data: UsuarioRolCreate, db: Session = Depends(get_db)):
    return create_usuario_rol(db, data)


@router.put(
    "/{ur_id}",
    response_model=UsuarioRolResponse,
    dependencies=[Depends(require_permission("seguridad_usuario_rol_asignar"))]
)
def actualizar_usuario_rol(ur_id: int, data: UsuarioRolUpdate, db: Session = Depends(get_db)):
    return update_usuario_rol(db, ur_id, data)


@router.delete(
    "/{ur_id}",
    dependencies=[Depends(require_permission("seguridad_usuario_rol_asignar"))]
)
def eliminar_usuario_rol(ur_id: int, db: Session = Depends(get_db)):
    delete_usuario_rol(db, ur_id)
    return {"detail": "Asignación usuario-rol eliminada correctamente"}
