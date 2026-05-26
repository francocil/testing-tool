from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from models.proyecto_documento import ProyectoDocumento

from services.file_service import save_file, replace_file, delete_file


# -----------------------------
# Listar documentos de proyecto
# -----------------------------
def get_proyecto_documentos(db: Session) -> list[ProyectoDocumento]:
    return db.query(ProyectoDocumento).all()


# -----------------------------
# Obtener documento por ID
# -----------------------------
def get_proyecto_documento(db: Session, documento_id: int) -> ProyectoDocumento:
    documento = (
        db.query(ProyectoDocumento)
        .filter(ProyectoDocumento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento de proyecto no encontrado"
        )

    return documento


# -----------------------------
# Crear documento de proyecto
# -----------------------------
def create_proyecto_documento(
    db: Session,
    proyecto_id: int,
    archivo: UploadFile,
    descripcion: str | None = None
) -> ProyectoDocumento:

    ruta_archivo = save_file(archivo, "documentos_proyecto")

    nuevo = ProyectoDocumento(
        proyecto_id=proyecto_id,
        archivo_url=ruta_archivo,
        descripcion=descripcion
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# -----------------------------
# Actualizar documento de proyecto
# -----------------------------
def update_proyecto_documento(
    db: Session,
    documento_id: int,
    archivo: UploadFile | None = None,
    descripcion: str | None = None
) -> ProyectoDocumento:

    documento = get_proyecto_documento(db, documento_id)

    if archivo is not None:
        documento.archivo_url = replace_file(
            documento.archivo_url,
            archivo,
            "documentos_proyecto"
        )

    if descripcion is not None:
        documento.descripcion = descripcion

    db.commit()
    db.refresh(documento)

    return documento


# -----------------------------
# Eliminar documento de proyecto
# -----------------------------
def delete_proyecto_documento(db: Session, documento_id: int) -> None:
    documento = get_proyecto_documento(db, documento_id)

    delete_file(documento.archivo_url)

    db.delete(documento)
    db.commit()
