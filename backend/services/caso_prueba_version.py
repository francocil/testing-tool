from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.caso_prueba_version import CasoPruebaVersion
from schemas.caso_prueba_version import (
    CasoPruebaVersionCreate,
    CasoPruebaVersionUpdate
)


# -----------------------------
# Listar versiones
# -----------------------------
def get_caso_prueba_versiones(db: Session) -> list[CasoPruebaVersion]:
    return db.query(CasoPruebaVersion).all()


# -----------------------------
# Obtener versión por ID
# -----------------------------
def get_caso_prueba_version(db: Session, version_id: int) -> CasoPruebaVersion:
    version = (
        db.query(CasoPruebaVersion)
        .filter(CasoPruebaVersion.id == version_id)
        .first()
    )

    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Versión de caso de prueba no encontrada"
        )

    return version


# -----------------------------
# Crear versión
# -----------------------------
def create_caso_prueba_version(
    db: Session,
    data: CasoPruebaVersionCreate
) -> CasoPruebaVersion:

    nueva = CasoPruebaVersion(
        caso_id=data.caso_id,
        nro_version=data.nro_version,
        objetivo=data.objetivo,
        porcentaje_aceptacion=data.porcentaje_aceptacion
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# -----------------------------
# Actualizar versión
# -----------------------------
def update_caso_prueba_version(
    db: Session,
    version_id: int,
    data: CasoPruebaVersionUpdate
) -> CasoPruebaVersion:

    version = get_caso_prueba_version(db, version_id)

    if data.objetivo is not None:
        version.objetivo = data.objetivo

    if data.porcentaje_aceptacion is not None:
        version.porcentaje_aceptacion = data.porcentaje_aceptacion

    db.commit()
    db.refresh(version)
    return version


# -----------------------------
# Eliminar versión
# -----------------------------
def delete_caso_prueba_version(db: Session, version_id: int) -> None:
    version = get_caso_prueba_version(db, version_id)
    db.delete(version)
    db.commit()
