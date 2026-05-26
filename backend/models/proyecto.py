from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .modulo import Modulo
    from .proyecto_documento import ProyectoDocumento
    from .usuario_proyecto import UsuarioProyecto
    from .reparticion import Reparticion
    from .direccion import Direccion
    from .area import Area


class Proyecto(Base):
    """
    Representa un proyecto de testing dentro del sistema.

    Alineado al SRS/SDS:

    - Nombre
    - Objetivo general
    - Contexto
    - Estado (activo, inactivo, archivado, borrador)
    - Versión
    - Fechas de creación / actualización
    - Modelo institucional (Repartición / Dirección / Área)
    - Documentos adjuntos
    - Usuarios asignados
    """

    __tablename__ = "proyecto"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    objetivo_general: Mapped[str | None] = mapped_column(Text)

    contexto: Mapped[str | None] = mapped_column(Text)

    estado: Mapped[str] = mapped_column(
        String(50),
        default="activo",
        nullable=False
    )

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # -----------------------------
    # Modelo institucional
    # -----------------------------
    reparticion_id: Mapped[int | None] = mapped_column(
        ForeignKey("reparticion.id"),
        nullable=True
    )
    direccion_id: Mapped[int | None] = mapped_column(
        ForeignKey("direccion.id"),
        nullable=True
    )
    area_id: Mapped[int | None] = mapped_column(
        ForeignKey("area.id"),
        nullable=True
    )

    reparticion: Mapped["Reparticion"] = relationship(
        "Reparticion",
        back_populates="proyectos",
        lazy="selectin"
    )
    direccion: Mapped["Direccion"] = relationship(
        "Direccion",
        back_populates="proyectos",
        lazy="selectin"
    )
    area: Mapped["Area"] = relationship(
        "Area",
        back_populates="proyectos",
        lazy="selectin"
    )

    # -----------------------------
    # Relaciones funcionales
    # -----------------------------
    usuarios_relacion: Mapped[list["UsuarioProyecto"]] = relationship(
        "UsuarioProyecto",
        back_populates="proyecto",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    modulos: Mapped[list["Modulo"]] = relationship(
        "Modulo",
        back_populates="proyecto",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    documentos: Mapped[list["ProyectoDocumento"]] = relationship(
        "ProyectoDocumento",
        back_populates="proyecto",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Proyecto {self.id} {self.nombre}>"
