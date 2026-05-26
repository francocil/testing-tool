# ============================================================
#  RUTAS: DOCUMENTOS DE PROYECTO
# ============================================================

from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from db.session import get_db
from services.proyecto_documento import (
    get_proyecto_documentos,
    get_proyecto_documento,
    create_proyecto_documento,
    update_proyecto_documento,
    delete_proyecto_documento,
)

from schemas.proyecto_documento import ProyectoDocumentoResponse

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


router = APIRouter(prefix="/proyecto-documentos", tags=["ProyectoDocumentos"])


# ============================================================
# 1) LISTAR DOCUMENTOS (JSON)
# ------------------------------------------------------------
# Permiso requerido:
#   - ver_documentos
# ============================================================
@router.get(
    "/",
    response_model=list[ProyectoDocumentoResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def listar_documentos(db: Session = Depends(get_db)):
    return get_proyecto_documentos(db)


# ============================================================
# 2) DESCARGAR DOCUMENTO (ARCHIVO REAL)
# ------------------------------------------------------------
# Permiso requerido:
#   - ver_documentos
# ============================================================
@router.get(
    "/{documento_id}",
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def descargar_documento(documento_id: int, db: Session = Depends(get_db)):
    documento = get_proyecto_documento(db, documento_id)
    file_path = documento.archivo_url

    if not os.path.exists(file_path):
        return Response(status_code=404)

    filename = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=mime_type,
    )


# ============================================================
# 3) CREAR DOCUMENTO
# ------------------------------------------------------------
# Permiso requerido:
#   - crear_documentos
# ============================================================
@router.post(
    "/",
    response_model=ProyectoDocumentoResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_documentos"))]
)
def crear_documento(
    proyecto_id: int = Form(...),
    descripcion: str | None = Form(None),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_proyecto_documento(db, proyecto_id, archivo, descripcion)


# ============================================================
# 4) ACTUALIZAR DOCUMENTO
# ------------------------------------------------------------
# Permiso requerido:
#   - editar_documentos
# ============================================================
@router.put(
    "/{documento_id}",
    response_model=ProyectoDocumentoResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_documentos"))]
)
def actualizar_documento(
    documento_id: int,
    descripcion: str | None = Form(None),
    archivo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    return update_proyecto_documento(db, documento_id, archivo, descripcion)


# ============================================================
# 5) ELIMINAR DOCUMENTO
# ------------------------------------------------------------
# Permiso requerido:
#   - eliminar_documentos
# ============================================================
@router.delete(
    "/{documento_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_documentos"))]
)
def eliminar_documento(documento_id: int, db: Session = Depends(get_db)):
    delete_proyecto_documento(db, documento_id)
    return Response(status_code=204)
