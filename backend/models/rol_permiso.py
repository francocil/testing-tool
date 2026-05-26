from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .rol import Rol
    from .permiso import Permiso


# ============================================================
#  MODELO: ROL_PERMISO
# ------------------------------------------------------------
#  Tabla intermedia (many-to-many) entre:
#     - Rol
#     - Permiso
#
#  Un rol puede tener múltiples permisos.
#  Un permiso puede pertenecer a múltiples roles.
#
#  Esta tabla es fundamental para:
#     - Matriz de permisos
#     - Seguridad granular
# ============================================================
class RolPermiso(Base):
    __tablename__ = "rol_permiso"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    rol_id: Mapped[int] = mapped_column(
        ForeignKey("rol.id"),
        nullable=False,
        index=True
    )

    permiso_id: Mapped[int] = mapped_column(
        ForeignKey("permiso.id"),
        nullable=False,
        index=True
    )

    # Relaciones
    rol: Mapped["Rol"] = relationship("Rol", back_populates="permisos_relacion")
    permiso: Mapped["Permiso"] = relationship("Permiso", back_populates="roles_relacion")
