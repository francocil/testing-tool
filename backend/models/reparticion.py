from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .direccion import Direccion
    from .proyecto import Proyecto


class Reparticion(Base):
    __tablename__ = "reparticion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_modificacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    direcciones: Mapped[list["Direccion"]] = relationship(
        "Direccion",
        back_populates="reparticion",
        cascade="all, delete-orphan"
    )

    # ============================================================
    # RELACIÓN INVERSA CON PROYECTO (FALTABA)
    # ============================================================
    proyectos: Mapped[list["Proyecto"]] = relationship(
        "Proyecto",
        back_populates="reparticion",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Reparticion {self.id} {self.nombre}>"
