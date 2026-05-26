from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, TIMESTAMP, Enum, DateTime, func
from db.base import Base

if TYPE_CHECKING:
    from .usuario import Usuario
    from .ejecucion import Ejecucion


# -----------------------------
# ENUM institucional
# -----------------------------
class EntidadTipo(enum.Enum):
    """
    Enum que indica sobre qué entidad se realizó el comentario.
    Permite trazabilidad transversal en:
    - Caso de prueba
    - Paso
    - Ejecución
    - Objeto/Parámetro
    """
    CASO = "caso"
    PASO = "paso"
    EJECUCION = "ejecucion"
    OBJETO_PARAMETRO = "objeto_parametro"


class Comentario(Base):
    """
    Representa un comentario realizado por un usuario sobre una entidad del sistema.
    Los comentarios permiten comunicación entre tester y developer, registro de fallas,
    aclaraciones, observaciones y trazabilidad completa.

    Según el SRS, un comentario debe registrar:
    - Usuario que comenta
    - Entidad objetivo (caso, paso, ejecución, parámetro)
    - Texto del comentario
    - Fecha
    - Relación opcional con una ejecución
    """

    __tablename__ = "comentario"

    # Identificador único del comentario
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Usuario que realizó el comentario
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        index=True
    )

    # Ejecución asociada (opcional)
    ejecucion_id: Mapped[int | None] = mapped_column(
        ForeignKey("ejecucion.id"),
        nullable=True,
        index=True
    )

    # Tipo de entidad a la que pertenece el comentario
    entidad_tipo: Mapped[EntidadTipo] = mapped_column(
        Enum(EntidadTipo, name="entidadtipo_enum"),
        nullable=False
    )

    # ID de la entidad objetivo (caso, paso, ejecución o parámetro)
    entidad_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Texto del comentario
    comentario: Mapped[str] = mapped_column(Text, nullable=False)

    # Fecha del comentario
    fecha: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    # Relación con Usuario
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="comentarios"
    )

    # Relación opcional con Ejecucion
    ejecucion: Mapped["Ejecucion | None"] = relationship(
        "Ejecucion",
        back_populates="comentarios"
    )
