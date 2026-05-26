from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
#  BASE
# ============================================================

class RolPermisoBase(BaseModel):
    """
    Campos comunes entre creación y actualización.
    """
    rol_id: int
    permiso_id: int


# ============================================================
#  CREATE
# ============================================================

class RolPermisoCreate(RolPermisoBase):
    """
    Datos necesarios para asignar un permiso a un rol.
    """
    pass


# ============================================================
#  UPDATE
# ============================================================

class RolPermisoUpdate(BaseModel):
    """
    Datos permitidos para actualizar una asignación rol-permiso.
    """
    rol_id: Optional[int] = None
    permiso_id: Optional[int] = None


# ============================================================
#  RESPONSE
# ============================================================

class RolPermisoResponse(RolPermisoBase):
    """
    Representación completa de la asignación rol-permiso
    devuelta por la API.
    """
    id: int
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True
