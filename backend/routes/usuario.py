from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from core.permissions import require_permission

from services.usuario import (
    get_usuarios,
    get_usuario,
    create_usuario,
    update_usuario,
    delete_usuario,
)

from schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)

router = APIRouter(prefix="/usuario", tags=["Usuarios"])


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_usuario_ver"))]
)
def listar_usuarios(db: Session = Depends(get_db)):
    return get_usuarios(db)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_usuario_ver"))]
)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return get_usuario(db, usuario_id)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_usuario_crear"))]
)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return create_usuario(db, data)


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("seguridad_usuario_editar"))]
)
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    return update_usuario(db, usuario_id, data)


@router.delete(
    "/{usuario_id}",
    status_code=204,
    dependencies=[Depends(require_permission("seguridad_usuario_eliminar"))]
)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    delete_usuario(db, usuario_id)
    return Response(status_code=204)
