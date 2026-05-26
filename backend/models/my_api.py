from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from db.base import Base

if TYPE_CHECKING:
    from .objeto_parametro import ObjetoParametro
    from .usuario import Usuario
    from .api_version import ApiVersion
    from .paso import Paso


class Api(Base):
    __tablename__ = "api"

    # -----------------------------
    # Campos principales
    # -----------------------------
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    descripcion: Mapped[str | None] = mapped_column(Text)

    metodo: Mapped[str] = mapped_column(String(10), nullable=False)

    base_url: Mapped[str | None] = mapped_column(String(255))

    endpoint: Mapped[str] = mapped_column(Text, nullable=False)

    auth_tipo: Mapped[str] = mapped_column(String(20), default="none")

    auth_config: Mapped[str | None] = mapped_column(Text)

    headers_por_defecto: Mapped[str | None] = mapped_column(Text)

    body_ejemplo: Mapped[str | None] = mapped_column(Text)

    timeout_segundos: Mapped[int] = mapped_column(Integer, default=10)

    retries: Mapped[int] = mapped_column(Integer, default=0)

    version: Mapped[str] = mapped_column(String(20), default="v1")

    activo: Mapped[int] = mapped_column(Integer, default=1)

    # -----------------------------
    # Auditoría
    # -----------------------------
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    fecha_modificacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id")
    )

    modificado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id")
    )

    # -----------------------------
    # Relaciones
    # -----------------------------
    parametros: Mapped[list["ObjetoParametro"]] = relationship(
        "ObjetoParametro",
        back_populates="api",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    versiones: Mapped[list["ApiVersion"]] = relationship(
        "ApiVersion",
        back_populates="api",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    creado_por: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[creado_por_usuario_id],
        lazy="selectin"
    )

    modificado_por: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[modificado_por_usuario_id],
        lazy="selectin"
    )

    # Relación inversa con Paso
    pasos: Mapped[list["Paso"]] = relationship(
        "Paso",
        back_populates="api",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Api {self.id} {self.nombre} v={self.version}>"
