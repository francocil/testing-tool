from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, Float, DateTime
from db.base import Base

if TYPE_CHECKING:
    from .caso_prueba_version import CasoPruebaVersion
    from .paso import Paso
    from .ejecucion import Ejecucion
    from .modulo import Modulo


class CasoPrueba(Base):
    """
    Representa un caso de prueba dentro de un módulo.

    Alineado al SRS/SDS:

    - Versionado automático
    - Nombre
    - Objetivo general
    - Descripción detallada
    - Precondiciones
    - Postcondiciones
    - Estado (activo / inactivo / borrador)
    - Pasos
    - Porcentaje de aceptación
    """

    __tablename__ = "caso_prueba"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    modulo_id: Mapped[int] = mapped_column(
        ForeignKey("modulo.id"),
        nullable=False,
        index=True
    )

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    objetivo: Mapped[str | None] = mapped_column(Text)

    descripcion: Mapped[str | None] = mapped_column(Text)

    precondiciones: Mapped[str | None] = mapped_column(Text)

    postcondiciones: Mapped[str | None] = mapped_column(Text)

    estado: Mapped[str] = mapped_column(
        String(50),
        default="activo",
        nullable=False
    )

    version_actual: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    porcentaje_aceptacion: Mapped[float | None] = mapped_column(Float)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    versiones: Mapped[list["CasoPruebaVersion"]] = relationship(
        "CasoPruebaVersion",
        back_populates="caso_prueba",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    pasos: Mapped[list["Paso"]] = relationship(
        "Paso",
        back_populates="caso",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Paso.orden"
    )

    ejecuciones: Mapped[list["Ejecucion"]] = relationship(
        "Ejecucion",
        back_populates="caso",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    modulo: Mapped["Modulo"] = relationship(
        "Modulo",
        back_populates="casos_prueba",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<CasoPrueba {self.id} {self.nombre}>"
