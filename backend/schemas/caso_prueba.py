from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# ============================================================
#  BASE
# ============================================================

class CasoPruebaBase(BaseModel):
    nombre: str
    objetivo: Optional[str] = None
    descripcion: Optional[str] = None
    precondiciones: Optional[str] = None
    postcondiciones: Optional[str] = None

    estado: str = "activo"
    activo: bool = True

    porcentaje_aceptacion: Optional[float] = None


# ============================================================
#  CREATE
# ============================================================

class CasoPruebaCreate(CasoPruebaBase):
    modulo_id: int


# ============================================================
#  UPDATE
# ============================================================

class CasoPruebaUpdate(BaseModel):
    nombre: Optional[str] = None
    objetivo: Optional[str] = None
    descripcion: Optional[str] = None
    precondiciones: Optional[str] = None
    postcondiciones: Optional[str] = None

    estado: Optional[str] = None
    activo: Optional[bool] = None
    porcentaje_aceptacion: Optional[float] = None


# ============================================================
#  RESPONSE (DETALLE)
# ============================================================

class CasoPruebaResponse(CasoPruebaBase):
    id: int
    modulo_id: int

    version_actual: int

    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
#  RESPONSE CON PASOS (DETALLE COMPLETO)
# ============================================================

class PasoSimple(BaseModel):
    id: int
    nombre: str
    orden: int

    class Config:
        from_attributes = True


class CasoPruebaWithPasos(CasoPruebaResponse):
    pasos: List[PasoSimple] = Field(default_factory=list)


# ============================================================
#  MAIN SCHEMA (LECTURA COMPLETA)
# ============================================================

class CasoPrueba(CasoPruebaResponse):
    """Schema principal de CasoPrueba (lectura completa)."""
    pass
