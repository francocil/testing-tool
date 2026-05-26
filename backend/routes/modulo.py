from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from db.session import get_db

from services.modulo import (
    get_modulo,
    list_modulos,
    create_modulo,
    update_modulo,
    delete_modulo,
)

from schemas.modulo import ModuloResponse, ModuloCreate, ModuloUpdate
from core.permissions import require_permission
from models.modulo import Modulo

router = APIRouter(prefix="/modulos", tags=["Módulos"])


# ===================================================
#  LISTAR MÓDULOS DE UN PROYECTO
# ===================================================
@router.get(
    "/",
    response_model=list[ModuloResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("modulo_ver_proyecto"))]
)
def listar_modulos(
    proyecto_id: int,
    nombre: str | None = None,
    tipo_interfaz: str | None = None,
    tipo_gui: str | None = None,
    estado: list[str] | None = None,
    limit: int = 20,
    offset: int = 0,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    return list_modulos(
        db=db,
        proyecto_id=proyecto_id,
        nombre=nombre,
        tipo_interfaz=tipo_interfaz,
        tipo_gui=tipo_gui,
        estado=estado,
        limit=limit,
        offset=offset,
        sort=sort
    )


# ==========================
#  OBTENER MÓDULO POR ID
# ==========================
@router.get(
    "/{modulo_id}",
    response_model=ModuloResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("modulo_ver_proyecto"))]
)
def obtener_modulo(modulo_id: int, db: Session = Depends(get_db)):
    return get_modulo(db, modulo_id)


# ==========================
#  CREAR MÓDULO
# ==========================
@router.post(
    "/",
    response_model=ModuloResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("modulo_crear"))]
)
def crear_modulo(data: ModuloCreate, db: Session = Depends(get_db)):
    return create_modulo(db, data)


# ==========================
#  ACTUALIZAR MÓDULO
# ==========================
@router.put(
    "/{modulo_id}",
    response_model=ModuloResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("modulo_editar"))]
)
def actualizar_modulo(modulo_id: int, data: ModuloUpdate, db: Session = Depends(get_db)):
    return update_modulo(db, modulo_id, data)


# ==========================
#  ELIMINAR MÓDULO
# ==========================
@router.delete(
    "/{modulo_id}",
    status_code=204,
    dependencies=[Depends(require_permission("modulo_eliminar"))]
)
def eliminar_modulo(modulo_id: int, db: Session = Depends(get_db)):
    delete_modulo(db, modulo_id)
    return Response(status_code=204)
