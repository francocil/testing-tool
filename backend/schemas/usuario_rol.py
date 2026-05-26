from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
#  BASE
# ============================================================

class UsuarioRolBase(BaseModel):
    """
    Campos comunes entre creación y actualización.
    """
    usuario_id: int
    rol_id: int


# ============================================================
#  CREATE
# ============================================================

class UsuarioRolCreate(UsuarioRolBase):
    """
    Datos necesarios para asignar un rol a un usuario.
    """
    pass


# ============================================================
#  UPDATE
# ============================================================

class UsuarioRolUpdate(BaseModel):
    """
    Datos permitidos para actualizar una asignación usuario-rol.
    """
    usuario_id: Optional[int] = None
    rol_id: Optional[int] = None


# ============================================================
#  RESPONSE
# ============================================================

class UsuarioRolResponse(UsuarioRolBase):
    """
    Representación completa de la asignación usuario-rol
    devuelta por la API.
    """
    id: int
    fecha_asignacion: Optional[datetime] = None

    class Config:
        from_attributes = True
