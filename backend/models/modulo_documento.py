from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .modulo import Modulo


class ModuloDocumento(Base):
    """
    Documento asociado a un módulo dentro de un proyecto de testing.
    Permite adjuntar archivos como manuales, capturas, especificaciones
    o cualquier documentación relevante al módulo funcional.

    Según el SRS, cada módulo puede tener múltiples documentos adjuntos.
    """

    __tablename__ = "modulo_documento"

    # Identificador único del documento
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Módulo al que pertenece el documento
    modulo_id: Mapped[int] = mapped_column(
        ForeignKey("modulo.id"),
        nullable=False,
        index=True
    )

    # URL o ruta del archivo almacenado
    archivo_url: Mapped[str] = mapped_column(Text, nullable=False)

    # Fecha en que se adjuntó el documento
    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relación hacia Modulo (muchos documentos → un módulo)
    modulo: Mapped["Modulo"] = relationship(
        "Modulo",
        back_populates="documentos"
    )
