"""
Rutas para la gestión de documentos asociados a pasos de prueba.
"""

from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from db.session import get_db
from services.paso_documento import (
    get_paso_documentos,
    get_paso_documento,
    create_paso_documento,
    update_paso_documento,
    delete_paso_documento,
)

from schemas.paso_documento import PasoDocumentoResponse

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


# ============================================================
# CONFIGURACIÓN DEL ROUTER
# ============================================================
router = APIRouter(prefix="/pasos-documentos", tags=["PasoDocumentos"])


# ============================================================
# LISTAR DOCUMENTOS (JSON)
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_documentos"
# ============================================================
@router.get(
    "/",
    response_model=list[PasoDocumentoResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def listar_paso_documentos(
    paso_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_paso_documentos(db, paso_id)


# ============================================================
# DESCARGAR DOCUMENTO (ARCHIVO REAL)
# ------------------------------------------------------------
#  Permiso requerido:
#     - "ver_documentos"
# ============================================================
@router.get(
    "/{documento_id}",
    dependencies=[Depends(require_permission("ver_documentos"))]
)
def descargar_paso_documento(documento_id: int, db: Session = Depends(get_db)):
    documento = get_paso_documento(db, documento_id)
    file_path = documento.archivo_url

    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path.lstrip("/"))

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
#  Permiso requerido:
#     - "crear_documentos"
# ============================================================
@router.post(
    "/",
    response_model=PasoDocumentoResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_documentos"))]
)
def crear_paso_documento_endpoint(
    paso_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_paso_documento(db, paso_id, archivo)


# ============================================================
# ACTUALIZAR DOCUMENTO
# ------------------------------------------------------------
#  Permiso requerido:
#     - "editar_documentos"
# ============================================================
@router.put(
    "/{documento_id}",
    response_model=PasoDocumentoResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_documentos"))]
)
def actualizar_paso_documento_endpoint(
    documento_id: int,
    archivo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    return update_paso_documento(db, documento_id, archivo)


# ============================================================
# ELIMINAR DOCUMENTO
# ------------------------------------------------------------
#  Permiso requerido:
#     - "eliminar_documentos"
# ============================================================
@router.delete(
    "/{documento_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_documentos"))]
)
def eliminar_paso_documento_endpoint(documento_id: int, db: Session = Depends(get_db)):
    delete_paso_documento(db, documento_id)
    return Response(status_code=204)
