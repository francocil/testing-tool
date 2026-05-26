from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ============================================================
#  BASE
# ============================================================

class ModuloBase(BaseModel):
    nombre: str
    tipo_interfaz: str
    tipo_gui: str
    descripcion: Optional[str] = None

    estado: str = "activo"
    activo: bool = True

    responsable_id: Optional[int] = None
    version: int = 1


# ============================================================
#  CREATE
# ============================================================

class ModuloCreate(ModuloBase):
    proyecto_id: int


# ============================================================
#  UPDATE
# ============================================================

class ModuloUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_interfaz: Optional[str] = None
    tipo_gui: Optional[str] = None
    descripcion: Optional[str] = None

    estado: Optional[str] = None
    activo: Optional[bool] = None
    responsable_id: Optional[int] = None
    version: Optional[int] = None


# ============================================================
#  RESPONSE
# ============================================================

class ModuloResponse(ModuloBase):
    id: int
    proyecto_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
#  MAIN SCHEMA (LECTURA COMPLETA)
# ============================================================

class Modulo(ModuloResponse):
    """Schema principal de Modulo (lectura completa)."""
    pass
