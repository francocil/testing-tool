from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from db.base import Base

if TYPE_CHECKING:
    from .my_api import Api
    from .usuario import Usuario


class ApiVersion(Base):
    """
    Historial de versiones de una API.
    Cada vez que se edita una API, se genera una nueva versión.
    La tabla API mantiene solo la versión activa.
    """

    __tablename__ = "api_version"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    api_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("api.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    version: Mapped[str] = mapped_column(String(20), nullable=False)

    metodo: Mapped[str] = mapped_column(String(10), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(255))
    endpoint: Mapped[str] = mapped_column(Text, nullable=False)

    auth_tipo: Mapped[str] = mapped_column(String(20), default="none")
    auth_config: Mapped[str | None] = mapped_column(Text)

    headers_por_defecto: Mapped[str | None] = mapped_column(Text)
    body_ejemplo: Mapped[str | None] = mapped_column(Text)

    timeout_segundos: Mapped[int] = mapped_column(Integer, default=10)
    retries: Mapped[int] = mapped_column(Integer, default=0)

    # -----------------------------
    # Auditoría
    # -----------------------------
    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("usuario.id")
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    api: Mapped["Api"] = relationship(
        "Api",
        back_populates="versiones",
        lazy="selectin"
    )

    creado_por: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[creado_por_usuario_id],
        lazy="selectin"
    )

    def __repr__(self):
        return f"<ApiVersion {self.id} api={self.api_id} v={self.version}>"
