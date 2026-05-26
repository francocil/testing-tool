# ============================================================
#  MODELO: Paso
# ------------------------------------------------------------
#  Representa una acción dentro de un caso de prueba.
#  Cada paso puede ser:
#   - manual
#   - automatico
#   - mixto
#   - simulado
#
#  Puede tener:
#   - API asociada
#   - parámetros JSON
#   - extracción de variables al contexto
#   - asserts
#   - documentos
#   - ejecuciones
# ============================================================

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, JSON
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .caso_prueba import CasoPrueba
    from .ejecucion_paso import EjecucionPaso
    from .objeto_parametro import ObjetoParametro
    from .paso_documento import PasoDocumento
    from .paso_assert import PasoAssert
    from .my_api import Api


class Paso(Base):
    __tablename__ = "paso"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    caso_id: Mapped[int] = mapped_column(
        ForeignKey("caso_prueba.id"),
        nullable=False,
        index=True
    )

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)

    api_id: Mapped[int | None] = mapped_column(
        ForeignKey("api.id"),
        nullable=True
    )

    api: Mapped["Api"] = relationship(
        "Api",
        back_populates="pasos",
        lazy="selectin"
    )

    orden: Mapped[int] = mapped_column(Integer, nullable=False)

    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    parametros_json: Mapped[dict | None] = mapped_column(JSON)

    extraccion_contexto: Mapped[dict | None] = mapped_column(JSON)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    caso: Mapped["CasoPrueba"] = relationship(
        "CasoPrueba",
        back_populates="pasos",
        lazy="selectin"
    )

    ejecuciones: Mapped[list["EjecucionPaso"]] = relationship(
        "EjecucionPaso",
        back_populates="paso",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # Parámetros legacy (ObjetoParametro)
    parametros: Mapped[list["ObjetoParametro"]] = relationship(
        "ObjetoParametro",
        back_populates="paso",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ObjetoParametro.id"
    )

    documentos: Mapped[list["PasoDocumento"]] = relationship(
        "PasoDocumento",
        back_populates="paso",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    asserts: Mapped[list["PasoAssert"]] = relationship(
        "PasoAssert",
        back_populates="paso",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="PasoAssert.orden"
    )

    def __repr__(self):
        return f"<Paso {self.id} {self.nombre}>"
