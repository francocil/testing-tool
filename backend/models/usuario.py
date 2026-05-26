from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, Boolean
from db.base import Base

if TYPE_CHECKING:
    from .usuario_proyecto import UsuarioProyecto
    from .proyecto import Proyecto
    from .ejecucion import Ejecucion
    from .comentario import Comentario
    from .usuario_rol import UsuarioRol
    from .agente import Agente
    from .modulo import Modulo


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # ============================================================
    # AGENTE ASOCIADO
    # ============================================================
    agente_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agentes.id"),
        nullable=True
    )

    agente: Mapped["Agente"] = relationship(
        "Agente",
        back_populates="usuarios",
        lazy="joined",
        foreign_keys=[agente_id]
    )

    # ============================================================
    # RELACIÓN INVERSA: MÓDULOS DONDE ES RESPONSABLE
    # ============================================================
    modulos_responsables: Mapped[list["Modulo"]] = relationship(
        "Modulo",
        back_populates="responsable",
        cascade="all, delete-orphan"
    )

    # ============================================================
    # OTRAS RELACIONES
    # ============================================================
    roles_relacion: Mapped[list["UsuarioRol"]] = relationship(
        "UsuarioRol",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    proyectos_relacion: Mapped[list["UsuarioProyecto"]] = relationship(
        "UsuarioProyecto",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    ejecuciones: Mapped[list["Ejecucion"]] = relationship(
        "Ejecucion",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    comentarios: Mapped[list["Comentario"]] = relationship(
        "Comentario",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
