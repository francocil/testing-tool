from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ============================================================
#  BASE
# ============================================================

class AreaBase(BaseModel):
    direccion_id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class AreaCreate(AreaBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class AreaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class AreaResponse(AreaBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True
