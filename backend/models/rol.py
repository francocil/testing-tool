from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from db.base import Base

if TYPE_CHECKING:
    from .usuario_rol import UsuarioRol
    from .rol_permiso import RolPermiso


# ============================================================
#  MODELO: ROL
# ------------------------------------------------------------
#  Representa un rol dentro del sistema.
#
#  Cambios en Iteración B:
#     - Un rol puede estar asignado a múltiples usuarios
#       mediante la tabla intermedia UsuarioRol.
#     - Un rol puede tener múltiples permisos asociados
#       mediante la tabla intermedia RolPermiso.
#
#  Cadena de seguridad:
#     Usuario → UsuarioRol → Rol → RolPermiso → Permiso
# ============================================================
class Rol(Base):
    __tablename__ = "rol"

    # Identificador único del rol
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Nombre del rol (Admin, Tester, Developer, etc.)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # ============================================================
    #  RELACIÓN: USUARIOS ASIGNADOS A ESTE ROL
    # ------------------------------------------------------------
    #  Un rol puede estar asignado a múltiples usuarios.
    #  La relación se maneja mediante la tabla UsuarioRol.
    # ============================================================
    usuarios_relacion: Mapped[list["UsuarioRol"]] = relationship(
        "UsuarioRol",
        back_populates="rol",
        cascade="all, delete-orphan"
    )

    # ============================================================
    #  RELACIÓN: PERMISOS ASOCIADOS AL ROL
    # ------------------------------------------------------------
    #  Un rol puede tener múltiples permisos.
    #  La relación se maneja mediante la tabla RolPermiso.
    # ============================================================
    permisos_relacion: Mapped[list["RolPermiso"]] = relationship(
        "RolPermiso",
        back_populates="rol",
        cascade="all, delete-orphan"
    )
