from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .paso import Paso


class PasoDocumento(Base):
    """
    Documento o evidencia asociada a un paso de un caso de prueba.
    Se utiliza para almacenar capturas, imágenes, PDFs o cualquier archivo
    que respalde la ejecución o definición del paso.

    Según el SRS, cada paso puede tener múltiples evidencias adjuntas.
    """

    __tablename__ = "paso_documento"

    # Identificador único del documento
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Paso al que pertenece el documento
    paso_id: Mapped[int] = mapped_column(
        ForeignKey("paso.id"),
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

    # Relación hacia Paso (muchos documentos → un paso)
    paso: Mapped["Paso"] = relationship(
        "Paso",
        back_populates="documentos"
    )
