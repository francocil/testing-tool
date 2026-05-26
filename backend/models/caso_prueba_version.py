from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, Float, DateTime, func

from db.base import Base

if TYPE_CHECKING:
    from .caso_prueba import CasoPrueba


class CasoPruebaVersion(Base):
    """
    Representa una versión histórica de un caso de prueba.
    Cada vez que un caso se modifica, se genera una nueva versión
    para mantener trazabilidad completa, tal como exige el SRS.

    Esta tabla almacena:
    - Número de versión
    - Objetivo en ese momento
    - Porcentaje de aceptación vigente
    - Fecha de creación de la versión
    """

    __tablename__ = "caso_prueba_version"

    # Identificador único de la versión
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Caso de prueba al que pertenece esta versión
    caso_id: Mapped[int] = mapped_column(
        ForeignKey("caso_prueba.id"),
        nullable=False,
        index=True
    )

    # Número de versión (incremental)
    nro_version: Mapped[int] = mapped_column(Integer, nullable=False)

    # Objetivo del caso en esta versión
    objetivo: Mapped[str | None] = mapped_column(Text)

    # Porcentaje de aceptación vigente en esta versión
    porcentaje_aceptacion: Mapped[float | None] = mapped_column(Float)

    # Fecha en que se creó esta versión
    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relación hacia CasoPrueba (muchas versiones → un caso)
    caso_prueba: Mapped["CasoPrueba"] = relationship(
        "CasoPrueba",
        back_populates="versiones",
        lazy="selectin"
    )
