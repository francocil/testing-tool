from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .direccion import Direccion
    from .agente import Agente
    from .proyecto import Proyecto


class Area(Base):
    __tablename__ = "area"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    direccion_id: Mapped[int] = mapped_column(ForeignKey("direccion.id"), nullable=False)

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    direccion: Mapped["Direccion"] = relationship(
        "Direccion",
        back_populates="areas"
    )

    agentes: Mapped[list["Agente"]] = relationship(
        "Agente",
        back_populates="area",
        cascade="all, delete-orphan"
    )

    # ============================================================
    # RELACIÓN INVERSA CON PROYECTO (FALTABA)
    # ============================================================
    proyectos: Mapped[list["Proyecto"]] = relationship(
        "Proyecto",
        back_populates="area",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Area {self.id} {self.nombre}>"
