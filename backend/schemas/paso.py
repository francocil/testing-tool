from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


# ============================================================
#  BASE
# ============================================================

class PasoBase(BaseModel):
    nombre: str
    tipo: str  # manual | automatico | mixto | simulado
    descripcion: str
    orden: int

    api_id: Optional[int] = None

    parametros_json: Optional[Dict[str, Any]] = None
    extraccion_contexto: Optional[Dict[str, Any]] = None

    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class PasoCreate(PasoBase):
    caso_id: int


# ============================================================
#  UPDATE
# ============================================================

class PasoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    orden: Optional[int] = None

    api_id: Optional[int] = None

    parametros_json: Optional[Dict[str, Any]] = None
    extraccion_contexto: Optional[Dict[str, Any]] = None

    activo: Optional[bool] = None


# ============================================================
#  RESPONSE (DETALLE)
# ============================================================

class PasoResponse(PasoBase):
    id: int
    caso_id: int

    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
#  RESPONSE CON ASSERTS (DETALLE COMPLETO)
# ============================================================

class PasoAssertSimple(BaseModel):
    id: int
    tipo: str
    expresion: Optional[str]
    operador: str
    valor_esperado: Optional[str]
    mensaje_error: Optional[str]
    orden: int

    class Config:
        from_attributes = True


class PasoWithAsserts(PasoResponse):
    asserts: List[PasoAssertSimple] = Field(default_factory=list)

# ============================================================
#  MAIN SCHEMA (LECTURA COMPLETA)
# ============================================================

class Paso(PasoResponse):
    """Schema principal de CasoPrueba (lectura completa)."""
    pass
