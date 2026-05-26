from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from db.session import get_db
from services.modulo_documento import (
    get_modulo_documentos,
    get_modulo_documento,
    create_modulo_documento,
    update_modulo_documento,
    delete_modulo_documento,
)

from schemas.modulo_documento import ModuloDocumentoResponse

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


# ============================================================
# CONFIGURACIÓN DEL ROUTER
# ============================================================
router = APIRouter(prefix="/modulo-documentos", tags=["ModuloDocumentos"])


# ============================================================
# LISTAR DOCUMENTOS (JSON)
# ------------------------------------------------------------
# Permiso requerido:
#   - ver_documentos
# ============================================================
@router.get(
    "/",
    response_model=list[ModuloDocumentoResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def listar_documentos(db: Session = Depends(get_db)):
    return get_modulo_documentos(db)


# ============================================================
# DESCARGAR DOCUMENTO (ARCHIVO REAL)
# ------------------------------------------------------------
# Permiso requerido:
#   - ver_documentos
# ============================================================
@router.get(
    "/{documento_id}",
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def descargar_documento(documento_id: int, db: Session = Depends(get_db)):
    documento = get_modulo_documento(db, documento_id)
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
# CREAR DOCUMENTO
# ------------------------------------------------------------
# Permiso requerido:
#   - crear_documentos
# ============================================================
@router.post(
    "/",
    response_model=ModuloDocumentoResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_documentos"))]
)
def crear_documento(
    modulo_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_modulo_documento(db, modulo_id, archivo)


# ============================================================
# ACTUALIZAR DOCUMENTO
# ------------------------------------------------------------
# Permiso requerido:
#   - editar_documentos
# ============================================================
@router.put(
    "/{documento_id}",
    response_model=ModuloDocumentoResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_documentos"))]
)
def actualizar_documento(
    documento_id: int,
    archivo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    return update_modulo_documento(db, documento_id, archivo)


# ============================================================
# ELIMINAR DOCUMENTO
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
    delete_modulo_documento(db, documento_id)
    return Response(status_code=204)
