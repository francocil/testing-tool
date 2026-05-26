from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
#  BASE
# ============================================================

class ProyectoDocumentoBase(BaseModel):
    proyecto_id: int
    archivo_url: str
    descripcion: Optional[str] = None


# ============================================================
#  CREATE
# ============================================================

class ProyectoDocumentoCreate(ProyectoDocumentoBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class ProyectoDocumentoUpdate(BaseModel):
    archivo_url: Optional[str] = None
    descripcion: Optional[str] = None


# ============================================================
#  RESPONSE
# ============================================================

class ProyectoDocumentoResponse(ProyectoDocumentoBase):
    id: int
    fecha_subida: datetime

    creado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True
