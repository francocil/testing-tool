from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Text, TIMESTAMP, Float, String, func, JSON
from db.base import Base

if TYPE_CHECKING:
    from .usuario import Usuario
    from .caso_prueba import CasoPrueba
    from .ejecucion_paso import EjecucionPaso
    from .comentario import Comentario


class Ejecucion(Base):
    """
    Representa la ejecución de un caso de prueba.
    Guarda snapshot del caso, contexto, pasos ejecutados,
    modo, estado, duración y resultado global.
    """

    __tablename__ = "ejecucion"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    caso_id: Mapped[int] = mapped_column(
        ForeignKey("caso_prueba.id"),
        nullable=False,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        index=True
    )

    fecha: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    fecha_fin: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True
    )

    duracion_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    modo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="mixto"
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pendiente"
    )

    resultado_global: Mapped[str | None] = mapped_column(String(50))

    porcentaje_aceptacion: Mapped[float | None] = mapped_column(Float)

    contexto: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    # -----------------------------
    # Snapshot del caso ejecutado
    # -----------------------------
    caso_version: Mapped[int] = mapped_column(Integer, nullable=False)
    caso_nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    caso_objetivo: Mapped[str | None] = mapped_column(Text)
    caso_precondiciones: Mapped[str | None] = mapped_column(Text)
    caso_postcondiciones: Mapped[str | None] = mapped_column(Text)

    # -----------------------------
    # Relaciones
    # -----------------------------
    caso: Mapped["CasoPrueba"] = relationship(
        "CasoPrueba",
        back_populates="ejecuciones",
        lazy="selectin"
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="ejecuciones",
        lazy="selectin"
    )

    pasos: Mapped[list["EjecucionPaso"]] = relationship(
        "EjecucionPaso",
        back_populates="ejecucion",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    comentarios: Mapped[list["Comentario"]] = relationship(
        "Comentario",
        back_populates="ejecucion",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Ejecucion {self.id} caso={self.caso_id} modo={self.modo}>"
