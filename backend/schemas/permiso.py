from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# ============================================================
#  BASE
# ============================================================

class PermisoBase(BaseModel):
    """
    Campos comunes entre creación y actualización.
    """
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class PermisoCreate(PermisoBase):
    """
    Datos necesarios para crear un permiso.
    """
    pass


# ============================================================
#  UPDATE
# ============================================================

class PermisoUpdate(BaseModel):
    """
    Datos permitidos para actualizar un permiso.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class PermisoResponse(PermisoBase):
    """
    Representación completa del permiso devuelta por la API.
    """
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    class Config:
        from_attributes = True
