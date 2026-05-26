from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .usuario import Usuario
    from .proyecto import Proyecto


class UsuarioProyecto(Base):
    """
    Representa la asignación de un usuario a un proyecto.
    Esta tabla intermedia permite controlar qué usuarios pueden ver
    o modificar cada proyecto, según su rol (Admin, Tester, Developer).

    Un usuario puede estar asignado a múltiples proyectos,
    y un proyecto puede tener múltiples usuarios asignados.
    """

    __tablename__ = "usuario_proyecto"

    # Identificador único de la relación usuario-proyecto
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID del usuario asignado al proyecto
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        index=True
    )

    # ID del proyecto al que está asignado el usuario
    proyecto_id: Mapped[int] = mapped_column(
        ForeignKey("proyecto.id"),
        nullable=False,
        index=True
    )

    # Fecha en que se asignó el usuario al proyecto
    fecha_asignacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relación hacia Usuario (muchos-a-uno)
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="proyectos_relacion"
    )

    # Relación hacia Proyecto (muchos-a-uno)
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="usuarios_relacion"
    )
