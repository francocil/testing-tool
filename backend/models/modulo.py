from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .modulo_documento import ModuloDocumento
    from .caso_prueba import CasoPrueba
    from .proyecto import Proyecto
    from .usuario import Usuario


class Modulo(Base):
    """
    Representa un módulo dentro de un proyecto de testing.

    Alineado al SRS/SDS:

    - Tipo de interfaz (pantalla, SQL, script, API, etc.)
    - Tipo de GUI (web, desktop, mobile, etc.)
    - Estado (activo, inactivo, archivado, borrador)
    - Responsable del módulo
    - Versionado
    - Documentos adjuntos
    - Casos de prueba
    """

    __tablename__ = "modulo"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    proyecto_id: Mapped[int] = mapped_column(
        ForeignKey("proyecto.id"),
        nullable=False,
        index=True
    )

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    tipo_interfaz: Mapped[str] = mapped_column(String(100), nullable=False)

    tipo_gui: Mapped[str] = mapped_column(String(100), nullable=False)

    descripcion: Mapped[str | None] = mapped_column(Text)

    estado: Mapped[str] = mapped_column(
        String(50),
        default="activo",
        nullable=False
    )

    responsable_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=True
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
    # Relaciones
    # -----------------------------
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="modulos",
        lazy="selectin"
    )

    responsable: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="modulos_responsables",
        lazy="selectin"
    )

    documentos: Mapped[list["ModuloDocumento"]] = relationship(
        "ModuloDocumento",
        back_populates="modulo",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    casos_prueba: Mapped[list["CasoPrueba"]] = relationship(
        "CasoPrueba",
        back_populates="modulo",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Modulo {self.id} {self.nombre}>"
