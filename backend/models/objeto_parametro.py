from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, String, ForeignKey, DateTime
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .paso import Paso
    from .my_api import Api


class ObjetoParametro(Base):
    __tablename__ = "objeto_parametro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    paso_id: Mapped[int | None] = mapped_column(
        ForeignKey("paso.id"),
        nullable=True,
        index=True
    )

    api_id: Mapped[int | None] = mapped_column(
        ForeignKey("api.id"),
        nullable=True,
        index=True
    )

    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    origen: Mapped[str] = mapped_column(String(20), default="api")

    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    valor_entrada: Mapped[str | None] = mapped_column(Text, nullable=True)
    valor_esperado: Mapped[str | None] = mapped_column(Text, nullable=True)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    paso: Mapped["Paso"] = relationship(
        "Paso",
        back_populates="parametros",
        lazy="selectin"
    )

    api: Mapped["Api"] = relationship(
        "Api",
        back_populates="parametros",
        lazy="selectin"
    )
