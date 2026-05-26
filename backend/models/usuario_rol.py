from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .usuario import Usuario
    from .rol import Rol


# ============================================================
#  MODELO: USUARIO_ROL
# ------------------------------------------------------------
#  Tabla intermedia (many-to-many) entre:
#     - Usuario
#     - Rol
#
#  Un usuario puede tener múltiples roles.
#  Un rol puede pertenecer a múltiples usuarios.
#
#  Esta tabla es fundamental para:
#     - Matriz de permisos
#     - Seguridad granular
#     - Scopes dinámicos
# ============================================================
class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    # ID único del registro
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Usuario asociado
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        index=True
    )

    # Rol asociado
    rol_id: Mapped[int] = mapped_column(
        ForeignKey("rol.id"),
        nullable=False,
        index=True
    )

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="roles_relacion"
    )

    rol: Mapped["Rol"] = relationship(
        "Rol",
        back_populates="usuarios_relacion"
    )
