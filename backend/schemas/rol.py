from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
#  BASE
# ============================================================

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class RolCreate(RolBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class RolResponse(RolBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    class Config:
        from_attributes = True
