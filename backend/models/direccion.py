from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .reparticion import Reparticion
    from .area import Area
    from .proyecto import Proyecto


class Direccion(Base):
    __tablename__ = "direccion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reparticion_id: Mapped[int] = mapped_column(ForeignKey("reparticion.id"), nullable=False)

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    reparticion: Mapped["Reparticion"] = relationship(
        "Reparticion",
        back_populates="direcciones"
    )

    areas: Mapped[list["Area"]] = relationship(
        "Area",
        back_populates="direccion",
        cascade="all, delete-orphan"
    )

    # ============================================================
    # RELACIÓN INVERSA CON PROYECTO (FALTABA)
    # ============================================================
    proyectos: Mapped[list["Proyecto"]] = relationship(
        "Proyecto",
        back_populates="direccion",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Direccion {self.id} {self.nombre}>"
