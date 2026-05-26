from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


# ============================================================
#  BASE
# ============================================================

class EjecucionBase(BaseModel):
    modo: str  # automatico | paso_a_paso | mixto | simulado
    estado: Optional[str] = None  # pendiente | en_progreso | finalizado | cancelado | error
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class EjecucionCreate(EjecucionBase):
    caso_id: int
    usuario_id: int


# ============================================================
#  UPDATE
# ============================================================

class EjecucionUpdate(BaseModel):
    modo: Optional[str] = None
    estado: Optional[str] = None
    resultado_global: Optional[str] = None
    porcentaje_aceptacion: Optional[float] = None
    contexto: Optional[Dict[str, Any]] = None
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE (DETALLE)
# ============================================================

class EjecucionResponse(EjecucionBase):
    id: int
    caso_id: int
    usuario_id: int

    modo: str
    estado: str = "pendiente"   # 🔥 FIX DEFINITIVO

    fecha: datetime
    fecha_fin: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    duracion_ms: Optional[int] = None

    resultado_global: Optional[str] = None
    porcentaje_aceptacion: Optional[float] = None

    contexto: Dict[str, Any]

    # Snapshot del caso
    caso_version: int
    caso_nombre: str
    caso_objetivo: Optional[str]
    caso_precondiciones: Optional[str]
    caso_postcondiciones: Optional[str]

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
#  RESPONSE CON PASOS (DETALLE COMPLETO)
# ============================================================

class EjecucionPasoSimple(BaseModel):
    id: int
    paso_id: int
    tipo_resultado: Optional[str]
    fecha: datetime

    class Config:
        from_attributes = True


class EjecucionWithPasos(EjecucionResponse):
    pasos: List[EjecucionPasoSimple] = Field(default_factory=list)

# ============================================================
#  MAIN SCHEMA (LECTURA COMPLETA)
# ============================================================

class Ejecucion(EjecucionResponse):
    """Schema principal de CasoPrueba (lectura completa)."""
    pass
