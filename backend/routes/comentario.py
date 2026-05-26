from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.comentario import (
    get_comentario,
    get_comentarios_por_entidad,
    create_comentario,
    update_comentario,
    delete_comentario,
)
from schemas.comentario import (
    ComentarioCreate,
    ComentarioUpdate,
    ComentarioResponse,
)
from models.comentario import EntidadTipo

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


router = APIRouter(prefix="/comentarios", tags=["Comentarios"])


# ============================================================
#  LISTAR COMENTARIOS POR ENTIDAD
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_documentos"
# ============================================================
@router.get(
    "/entidad/{entidad_tipo}/{entidad_id}",
    response_model=list[ComentarioResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def listar_comentarios_por_entidad(
    entidad_tipo: EntidadTipo,
    entidad_id: int,
    db: Session = Depends(get_db)
):
    return get_comentarios_por_entidad(db, entidad_tipo, entidad_id)


# ============================================================
#  OBTENER COMENTARIO POR ID
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_documentos"
# ============================================================
@router.get(
    "/{comentario_id}",
    response_model=ComentarioResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def obtener_comentario(comentario_id: int, db: Session = Depends(get_db)):
    return get_comentario(db, comentario_id)


# ============================================================
#  CREAR COMENTARIO
# ------------------------------------------------------------
#  Permiso requerido:
#     - "crear_documentos"
# ============================================================
@router.post(
    "/",
    response_model=ComentarioResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_documentos"))]
)
def crear_comentario(data: ComentarioCreate, db: Session = Depends(get_db)):
    return create_comentario(db, data)


# ============================================================
#  ACTUALIZAR COMENTARIO
# ------------------------------------------------------------
#  Permiso requerido:
#     - "editar_documentos"
# ============================================================
@router.put(
    "/{comentario_id}",
    response_model=ComentarioResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_documentos"))]
)
def actualizar_comentario(comentario_id: int, data: ComentarioUpdate, db: Session = Depends(get_db)):
    return update_comentario(db, comentario_id, data)


# ============================================================
#  ELIMINAR COMENTARIO
# ------------------------------------------------------------
#  Permiso requerido:
#     - "eliminar_documentos"
# ============================================================
@router.delete(
    "/{comentario_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_documentos"))]
)
def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    delete_comentario(db, comentario_id)
    return Response(status_code=204)
