"""
SERVICIO: paso_documento
------------------------------------------------------------
Maneja la lógica de negocio para documentos asociados a pasos.

MEJORAS IMPORTANTES:
- Se normaliza la ruta guardada en BD para que SIEMPRE sea relativa.
- Se documenta cada función con claridad.
- Se mantiene compatibilidad con rutas absolutas antiguas.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from models.paso_documento import PasoDocumento
from services.file_service import save_file, replace_file, delete_file


# ============================================================
# LISTAR DOCUMENTOS (con filtro opcional por paso_id)
# ============================================================
def get_paso_documentos(db: Session, paso_id: int | None = None) -> list[PasoDocumento]:
    """
    Devuelve todos los documentos, o solo los de un paso específico.
    """
    query = db.query(PasoDocumento)

    if paso_id is not None:
        query = query.filter(PasoDocumento.paso_id == paso_id)

    return query.order_by(PasoDocumento.fecha_subida.asc()).all()


# ============================================================
# OBTENER DOCUMENTO POR ID
# ============================================================
def get_paso_documento(db: Session, documento_id: int) -> PasoDocumento:
    """
    Devuelve un documento por su ID.
    Lanza 404 si no existe.
    """
    documento = (
        db.query(PasoDocumento)
        .filter(PasoDocumento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento de paso no encontrado"
        )

    return documento


# ============================================================
# CREAR DOCUMENTO
# ============================================================
def create_paso_documento(
    db: Session,
    paso_id: int,
    archivo: UploadFile
) -> PasoDocumento:
    """
    Crea un documento asociado a un paso.
    Guarda SIEMPRE una ruta relativa en la base.
    """

    # save_file devuelve una ruta relativa (garantizado)
    ruta_relativa = save_file(archivo, "documentos_paso")

    nuevo = PasoDocumento(
        paso_id=paso_id,
        archivo_url=ruta_relativa
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ============================================================
# ACTUALIZAR DOCUMENTO
# ============================================================
def update_paso_documento(
    db: Session,
    documento_id: int,
    archivo: UploadFile | None = None
) -> PasoDocumento:
    """
    Actualiza el archivo de un documento.
    Reemplaza el archivo físico y actualiza la ruta relativa.
    """

    documento = get_paso_documento(db, documento_id)

    if archivo is not None:
        # replace_file devuelve SIEMPRE una ruta relativa
        documento.archivo_url = replace_file(
            documento.archivo_url,
            archivo,
            "documentos_paso"
        )

    db.commit()
    db.refresh(documento)

    return documento


# ============================================================
# ELIMINAR DOCUMENTO
# ============================================================
def delete_paso_documento(db: Session, documento_id: int) -> None:
    """
    Elimina un documento y su archivo físico.
    """

    documento = get_paso_documento(db, documento_id)

    # delete_file acepta rutas relativas o absolutas
    delete_file(documento.archivo_url)

    db.delete(documento)
    db.commit()
