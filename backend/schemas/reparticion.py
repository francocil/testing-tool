from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ============================================================
#  BASE
# ============================================================

class ReparticionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class ReparticionCreate(ReparticionBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class ReparticionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class ReparticionResponse(ReparticionBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    class Config:
        from_attributes = True
