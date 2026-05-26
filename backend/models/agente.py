from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from db.base import Base

if TYPE_CHECKING:
    from .area import Area
    from .reparticion import Reparticion
    from .direccion import Direccion
    from .usuario import Usuario


class Agente(Base):
    __tablename__ = "agentes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(20), unique=True, nullable=False)
    cuil = Column(String(20), unique=True, nullable=False)
    apellido_nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    reparticion_id = Column(Integer, ForeignKey("reparticion.id"), nullable=False)
    direccion_id = Column(Integer, ForeignKey("direccion.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    cargo = Column(String(150), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_baja = Column(DateTime, nullable=True)

    creado_por_usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    modificado_por_usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True)

    # ============================================================
    # RELACIÓN INVERSA CON USUARIO
    # ============================================================
    usuarios = relationship(
        "Usuario",
        back_populates="agente",
        foreign_keys="Usuario.agente_id"
    )

    area = relationship("Area", back_populates="agentes")

    def __repr__(self):
        return f"<Agente {self.id} {self.apellido_nombre}>"
