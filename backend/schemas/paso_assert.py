from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# ============================================================
#  BASE
# ============================================================

class PasoAssertBase(BaseModel):
    tipo: str
    expresion: Optional[str] = None
    operador: str
    valor_esperado: Optional[str] = None
    mensaje_error: Optional[str] = None
    orden: int = 1

    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class PasoAssertCreate(PasoAssertBase):
    paso_id: int


# ============================================================
#  UPDATE
# ============================================================

class PasoAssertUpdate(BaseModel):
    tipo: Optional[str] = None
    expresion: Optional[str] = None
    operador: Optional[str] = None
    valor_esperado: Optional[str] = None
    mensaje_error: Optional[str] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class PasoAssertResponse(PasoAssertBase):
    id: int
    paso_id: int

    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True
