from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .proyecto import Proyecto


class ProyectoDocumento(Base):
    """
    Documento asociado a un proyecto de testing.
    Permite adjuntar archivos como especificaciones, imágenes, PDFs,
    evidencias o cualquier documentación relevante al proyecto.

    Según el SRS, cada proyecto puede tener múltiples documentos adjuntos.
    """

    __tablename__ = "proyecto_documento"

    # Identificador único del documento
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Proyecto al que pertenece el documento
    proyecto_id: Mapped[int] = mapped_column(
        ForeignKey("proyecto.id"),
        nullable=False,
        index=True
    )

    # URL o ruta del archivo almacenado
    archivo_url: Mapped[str] = mapped_column(Text, nullable=False)

    # Descripción opcional del documento (ej: "Diagrama de arquitectura")
    descripcion: Mapped[str | None] = mapped_column(Text)

    # Fecha en que se adjuntó el documento
    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relación hacia Proyecto (muchos-a-uno)
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="documentos"
    )
