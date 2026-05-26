from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

# Importar los schemas REALES según tu árbol
from schemas.reparticion import ReparticionResponse
from schemas.direccion import DireccionResponse
from schemas.area import AreaResponse
from schemas.proyecto_documento import ProyectoDocumentoResponse
from schemas.modulo import ModuloResponse
from schemas.usuario_proyecto import UsuarioProyectoResponse


# ============================================================
#  BASE
# ============================================================

class ProyectoBase(BaseModel):
    nombre: str
    objetivo_general: Optional[str] = None
    contexto: Optional[str] = None

    estado: str = "activo"
    activo: bool = True

    reparticion_id: Optional[int] = None
    direccion_id: Optional[int] = None
    area_id: Optional[int] = None


# ============================================================
#  CREATE
# ============================================================

class ProyectoCreate(ProyectoBase):
    """
    El cliente NO envía versión.
    La versión siempre inicia en 1 (lado backend).
    """
    pass


# ============================================================
#  UPDATE
# ============================================================

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    objetivo_general: Optional[str] = None
    contexto: Optional[str] = None

    estado: Optional[str] = None
    activo: Optional[bool] = None

    reparticion_id: Optional[int] = None
    direccion_id: Optional[int] = None
    area_id: Optional[int] = None


# ============================================================
#  RESPONSE
# ============================================================

class ProyectoResponse(ProyectoBase):
    id: int
    version: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    # Relaciones institucionales
    reparticion: Optional[ReparticionResponse] = None
    direccion: Optional[DireccionResponse] = None
    area: Optional[AreaResponse] = None

    # Relaciones funcionales
    documentos: List[ProyectoDocumentoResponse] = Field(default_factory=list)
    modulos: List[ModuloResponse] = Field(default_factory=list)
    usuarios_relacion: List[UsuarioProyectoResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
