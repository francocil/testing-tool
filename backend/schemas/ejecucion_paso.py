from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel


# ============================================================
#  BASE
# ============================================================

class EjecucionPasoBase(BaseModel):
    tipo_resultado: Optional[str] = None  # ok | fallo_assert | error_tecnico | simulado | manual_ok | manual_error
    request_json: Optional[Dict[str, Any]] = None
    response_json: Optional[Dict[str, Any]] = None
    asserts_json: Optional[List[Dict[str, Any]]] = None
    errores_json: Optional[List[str]] = None
    valor_obtenido: Optional[str] = None
    duracion_ms: Optional[float] = None

    # Snapshots
    parametros_snapshot: Optional[List[Dict[str, Any]]] = None
    asserts_snapshot: Optional[List[Dict[str, Any]]] = None

    # Auditoría
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class EjecucionPasoCreate(EjecucionPasoBase):
    ejecucion_id: int
    paso_id: int


# ============================================================
#  UPDATE
# ============================================================

class EjecucionPasoUpdate(BaseModel):
    tipo_resultado: Optional[str] = None
    request_json: Optional[Dict[str, Any]] = None
    response_json: Optional[Dict[str, Any]] = None
    asserts_json: Optional[List[Dict[str, Any]]] = None
    errores_json: Optional[List[str]] = None
    valor_obtenido: Optional[str] = None
    duracion_ms: Optional[float] = None

    parametros_snapshot: Optional[List[Dict[str, Any]]] = None
    asserts_snapshot: Optional[List[Dict[str, Any]]] = None

    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class EjecucionPasoResponse(EjecucionPasoBase):
    id: int
    ejecucion_id: int
    paso_id: int

    fecha: datetime
    fecha_actualizacion: Optional[datetime] = None

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

# ============================================================
#  MAIN SCHEMA (LECTURA COMPLETA)
# ============================================================

class EjecucionPaso(EjecucionPasoResponse):
    """Schema principal de CasoPrueba (lectura completa)."""
    pass
