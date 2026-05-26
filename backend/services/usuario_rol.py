# ============================================================
#  SERVICES: USUARIO_ROL
# ------------------------------------------------------------
#  Contiene la lógica de negocio para administrar la relación
#  entre:
#       - Usuario
#       - Rol
#
#  Operaciones incluidas:
#     - Listar asignaciones usuario-rol
#     - Obtener asignación por ID
#     - Crear asignación
#     - Actualizar asignación
#     - Eliminar asignación
#
#  Este service es utilizado por:
#     - Administración de usuarios
#     - Sistema de roles
#     - Motor de permisos
# ============================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.usuario_rol import UsuarioRol
from models.usuario import Usuario
from models.rol import Rol

from schemas.usuario_rol import (
    UsuarioRolCreate,
    UsuarioRolUpdate,
)


# ------------------------------------------------------------
#  LISTAR ASIGNACIONES USUARIO-ROL
# ------------------------------------------------------------
def get_usuarios_roles(db: Session) -> list[UsuarioRol]:
    """
    Devuelve todas las asignaciones usuario-rol.
    """
    return db.query(UsuarioRol).all()


# ------------------------------------------------------------
#  OBTENER ASIGNACIÓN POR ID
# ------------------------------------------------------------
def get_usuario_rol(db: Session, ur_id: int) -> UsuarioRol:
    """
    Devuelve una asignación usuario-rol específica.
    Lanza 404 si no existe.
    """
    ur = (
        db.query(UsuarioRol)
        .filter(UsuarioRol.id == ur_id)
        .first()
    )

    if not ur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación usuario-rol no encontrada"
        )

    return ur


# ------------------------------------------------------------
#  CREAR ASIGNACIÓN USUARIO-ROL
# ------------------------------------------------------------
def create_usuario_rol(db: Session, data: UsuarioRolCreate) -> UsuarioRol:
    """
    Crea una nueva asignación usuario-rol.
    Valida:
        - Que el usuario exista
        - Que el rol exista
        - Que la asignación no esté duplicada
    """

    # Validar existencia del usuario
    usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Validar existencia del rol
    rol = db.query(Rol).filter(Rol.id == data.rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    # Validar duplicado
    existente = (
        db.query(UsuarioRol)
        .filter(
            UsuarioRol.usuario_id == data.usuario_id,
            UsuarioRol.rol_id == data.rol_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya tiene asignado este rol"
        )

    nuevo = UsuarioRol(
        usuario_id=data.usuario_id,
        rol_id=data.rol_id,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ------------------------------------------------------------
#  ACTUALIZAR ASIGNACIÓN USUARIO-ROL
# ------------------------------------------------------------
def update_usuario_rol(db: Session, ur_id: int, data: UsuarioRolUpdate) -> UsuarioRol:
    """
    Actualiza una asignación usuario-rol existente.
    Solo modifica los campos enviados.
    """
    ur = get_usuario_rol(db, ur_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(ur, field, value)

    db.commit()
    db.refresh(ur)

    return ur


# ------------------------------------------------------------
#  ELIMINAR ASIGNACIÓN USUARIO-ROL
# ------------------------------------------------------------
def delete_usuario_rol(db: Session, ur_id: int) -> None:
    """
    Elimina una asignación usuario-rol del sistema.
    """
    ur = get_usuario_rol(db, ur_id)

    db.delete(ur)
    db.commit()
