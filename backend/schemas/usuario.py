from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .rol import RolResponse


# ============================================================
#  BASE
# ============================================================

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    agente_id: Optional[int] = None


# ============================================================
#  CREATE
# ============================================================

class UsuarioCreate(UsuarioBase):
    password: str
    # ❗ Ya NO se envía rol_id
    # Los roles se asignan vía /usuarios/{id}/roles


# ============================================================
#  UPDATE
# ============================================================

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    agente_id: Optional[int] = None
    # ❗ Ya NO existe rol_id aquí tampoco


# ============================================================
#  RESPONSE
# ============================================================

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    # Roles del usuario (N:N)
    roles: List[RolResponse]

    # Permisos efectivos (calculados)
    permisos: List[str] | None = None

    class Config:
        from_attributes = True
