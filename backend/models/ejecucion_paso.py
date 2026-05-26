from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Text, TIMESTAMP, Float, JSON, func
from db.base import Base

if TYPE_CHECKING:
    from .ejecucion import Ejecucion
    from .paso import Paso


class EjecucionPaso(Base):
    """
    Snapshot de la ejecución de un paso.
    Guarda:
    - request enviado
    - response recibido
    - asserts evaluados
    - errores técnicos
    - resultado final
    - duración
    """

    __tablename__ = "ejecucion_paso"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    ejecucion_id: Mapped[int] = mapped_column(
        ForeignKey("ejecucion.id"),
        nullable=False,
        index=True
    )

    paso_id: Mapped[int] = mapped_column(
        ForeignKey("paso.id"),
        nullable=False,
        index=True
    )

    tipo_resultado: Mapped[str | None] = mapped_column(Text)

    request_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    response_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    asserts_json: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)

    errores_json: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    valor_obtenido: Mapped[str | None] = mapped_column(Text)

    duracion_ms: Mapped[float | None] = mapped_column(Float)

    fecha: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    ejecucion: Mapped["Ejecucion"] = relationship(
        "Ejecucion",
        back_populates="pasos",
        lazy="selectin"
    )

    paso: Mapped["Paso"] = relationship(
        "Paso",
        back_populates="ejecuciones",
        lazy="selectin"
    )

    # -----------------------------
    # Snapshots del paso
    # -----------------------------
    parametros_snapshot: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)

    asserts_snapshot: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)

    def __repr__(self):
        return f"<EjecucionPaso {self.id} paso={self.paso_id} resultado={self.tipo_resultado}>"
