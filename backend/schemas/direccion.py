from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ============================================================
#  BASE
# ============================================================

class DireccionBase(BaseModel):
    reparticion_id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class DireccionCreate(DireccionBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class DireccionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class DireccionResponse(DireccionBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    class Config:
        from_attributes = True
