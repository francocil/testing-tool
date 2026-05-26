from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from models.modulo_documento import ModuloDocumento

from services.file_service import save_file, replace_file, delete_file


# -----------------------------
# Listar documentos de módulo
# -----------------------------
def get_modulo_documentos(db: Session) -> list[ModuloDocumento]:
    return db.query(ModuloDocumento).all()


# -----------------------------
# Obtener documento por ID
# -----------------------------
def get_modulo_documento(db: Session, documento_id: int) -> ModuloDocumento:
    documento = (
        db.query(ModuloDocumento)
        .filter(ModuloDocumento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento de módulo no encontrado"
        )

    return documento


# -----------------------------
# Crear documento de módulo
# -----------------------------
def create_modulo_documento(
    db: Session,
    modulo_id: int,
    archivo: UploadFile
) -> ModuloDocumento:

    ruta_archivo = save_file(archivo, "documentos_modulo")

    nuevo = ModuloDocumento(
        modulo_id=modulo_id,
        archivo_url=ruta_archivo
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# -----------------------------
# Actualizar documento de módulo
# -----------------------------
def update_modulo_documento(
    db: Session,
    documento_id: int,
    archivo: UploadFile | None = None
) -> ModuloDocumento:

    documento = get_modulo_documento(db, documento_id)

    if archivo is not None:
        documento.archivo_url = replace_file(
            documento.archivo_url,
            archivo,
            "documentos_modulo"
        )

    db.commit()
    db.refresh(documento)

    return documento


# -----------------------------
# Eliminar documento de módulo
# -----------------------------
def delete_modulo_documento(db: Session, documento_id: int) -> None:
    documento = get_modulo_documento(db, documento_id)

    delete_file(documento.archivo_url)

    db.delete(documento)
    db.commit()
