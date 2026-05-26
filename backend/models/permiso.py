from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from db.base import Base

if TYPE_CHECKING:
    from .rol_permiso import RolPermiso


# ============================================================
#  MODELO: PERMISO
# ------------------------------------------------------------
#  Representa una acción concreta dentro del sistema.
#  Ejemplos:
#     - crear_usuario
#     - editar_usuario
#     - eliminar_usuario
#     - ver_proyectos
#     - ejecutar_casos
#
#  Los permisos NO se asignan directamente a usuarios.
#  Se asignan a ROLES → y los roles se asignan a usuarios.
#
#  Este modelo es clave para:
#     - Matriz de permisos
#     - Seguridad granular
#     - Visibilidad dinámica por scope
# ============================================================
class Permiso(Base):
    __tablename__ = "permiso"

    # ID único del permiso
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Nombre interno del permiso (snake_case)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Descripción legible para humanos
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)

    # Indica si el permiso está activo
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relación con RolPermiso (muchos-a-muchos indirecto)
    roles_relacion: Mapped[list["RolPermiso"]] = relationship(
        "RolPermiso",
        back_populates="permiso",
        cascade="all, delete-orphan"
    )
