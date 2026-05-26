# ============================================================
#  SERVICES: ROL_PERMISO
# ------------------------------------------------------------
#  Contiene la lógica de negocio para administrar la relación
#  entre:
#       - Rol
#       - Permiso
#
#  Operaciones incluidas:
#     - Listar asignaciones rol-permiso
#     - Obtener asignación por ID
#     - Crear asignación
#     - Actualizar asignación
#     - Eliminar asignación
#
#  Este service es utilizado por:
#     - Administración de roles
#     - Matriz de permisos
#     - Sistema de seguridad
# ============================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.rol_permiso import RolPermiso
from models.rol import Rol
from models.permiso import Permiso

from schemas.rol_permiso import (
    RolPermisoCreate,
    RolPermisoUpdate,
)


# ------------------------------------------------------------
#  LISTAR ASIGNACIONES ROL-PERMISO
# ------------------------------------------------------------
def get_roles_permisos(db: Session) -> list[RolPermiso]:
    """
    Devuelve todas las asignaciones rol-permiso.
    """
    return db.query(RolPermiso).all()


# ------------------------------------------------------------
#  OBTENER ASIGNACIÓN POR ID
# ------------------------------------------------------------
def get_rol_permiso(db: Session, rp_id: int) -> RolPermiso:
    """
    Devuelve una asignación rol-permiso específica.
    Lanza 404 si no existe.
    """
    rp = (
        db.query(RolPermiso)
        .filter(RolPermiso.id == rp_id)
        .first()
    )

    if not rp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación rol-permiso no encontrada"
        )

    return rp


# ------------------------------------------------------------
#  CREAR ASIGNACIÓN ROL-PERMISO
# ------------------------------------------------------------
def create_rol_permiso(db: Session, data: RolPermisoCreate) -> RolPermiso:
    """
    Crea una nueva asignación rol-permiso.
    Valida:
        - Que el rol exista
        - Que el permiso exista
        - Que la asignación no esté duplicada
    """

    # Validar existencia del rol
    rol = db.query(Rol).filter(Rol.id == data.rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    # Validar existencia del permiso
    permiso = db.query(Permiso).filter(Permiso.id == data.permiso_id).first()
    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )

    # Validar duplicado
    existente = (
        db.query(RolPermiso)
        .filter(
            RolPermiso.rol_id == data.rol_id,
            RolPermiso.permiso_id == data.permiso_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol ya tiene asignado este permiso"
        )

    nuevo = RolPermiso(
        rol_id=data.rol_id,
        permiso_id=data.permiso_id,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ------------------------------------------------------------
#  ACTUALIZAR ASIGNACIÓN ROL-PERMISO
# ------------------------------------------------------------
def update_rol_permiso(db: Session, rp_id: int, data: RolPermisoUpdate) -> RolPermiso:
    """
    Actualiza una asignación rol-permiso existente.
    Solo modifica los campos enviados.
    """
    rp = get_rol_permiso(db, rp_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(rp, field, value)

    db.commit()
    db.refresh(rp)

    return rp


# ------------------------------------------------------------
#  ELIMINAR ASIGNACIÓN ROL-PERMISO
# ------------------------------------------------------------
def delete_rol_permiso(db: Session, rp_id: int) -> None:
    """
    Elimina una asignación rol-permiso del sistema.
    """
    rp = get_rol_permiso(db, rp_id)

    db.delete(rp)
    db.commit()
