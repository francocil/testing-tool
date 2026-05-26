from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .usuario import UsuarioResponse


# ============================================================
#  PROYECTO MINI (para evitar ciclos)
# ============================================================

class ProyectoMini(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


# ============================================================
#  BASE
# ============================================================

class UsuarioProyectoBase(BaseModel):
    usuario_id: int
    proyecto_id: int


# ============================================================
#  CREATE
# ============================================================

class UsuarioProyectoCreate(UsuarioProyectoBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class UsuarioProyectoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    proyecto_id: Optional[int] = None


# ============================================================
#  RESPONSE
# ============================================================

class UsuarioProyectoResponse(UsuarioProyectoBase):
    id: int
    fecha_asignacion: datetime

    usuario: UsuarioResponse
    proyecto: ProyectoMini

    class Config:
        from_attributes = True
