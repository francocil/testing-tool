# ============================================================
#  SERVICES: PERMISO
# ------------------------------------------------------------
#  Contiene la lógica de negocio para administrar permisos.
#  Operaciones incluidas:
#     - Listar permisos
#     - Obtener permiso por ID
#     - Crear permiso
#     - Actualizar permiso
#     - Eliminar permiso
#
#  Este service es utilizado por:
#     - Rutas de administración de permisos
#     - Sistema de roles y matriz de permisos
# ============================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.permiso import Permiso
from schemas.permiso import (
    PermisoCreate,
    PermisoUpdate,
)


# ------------------------------------------------------------
#  LISTAR PERMISOS
# ------------------------------------------------------------
def get_permisos(db: Session) -> list[Permiso]:
    """
    Devuelve todos los permisos registrados.
    """
    return db.query(Permiso).all()


# ------------------------------------------------------------
#  OBTENER PERMISO POR ID
# ------------------------------------------------------------
def get_permiso(db: Session, permiso_id: int) -> Permiso:
    """
    Devuelve un permiso específico por ID.
    Lanza 404 si no existe.
    """
    permiso = (
        db.query(Permiso)
        .filter(Permiso.id == permiso_id)
        .first()
    )

    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )

    return permiso


# ------------------------------------------------------------
#  CREAR PERMISO
# ------------------------------------------------------------
def create_permiso(db: Session, data: PermisoCreate) -> Permiso:
    """
    Crea un nuevo permiso.
    Valida que el nombre no exista previamente.
    """
    existente = (
        db.query(Permiso)
        .filter(Permiso.nombre == data.nombre)
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un permiso con ese nombre"
        )

    nuevo = Permiso(
        nombre=data.nombre,
        descripcion=data.descripcion,
        activo=data.activo,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ------------------------------------------------------------
#  ACTUALIZAR PERMISO
# ------------------------------------------------------------
def update_permiso(db: Session, permiso_id: int, data: PermisoUpdate) -> Permiso:
    """
    Actualiza un permiso existente.
    Solo modifica los campos enviados.
    """
    permiso = get_permiso(db, permiso_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(permiso, field, value)

    db.commit()
    db.refresh(permiso)

    return permiso


# ------------------------------------------------------------
#  ELIMINAR PERMISO
# ------------------------------------------------------------
def delete_permiso(db: Session, permiso_id: int) -> None:
    """
    Elimina un permiso del sistema.
    """
    permiso = get_permiso(db, permiso_id)

    db.delete(permiso)
    db.commit()
