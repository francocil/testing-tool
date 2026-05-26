from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .rol import RolResponse


# ============================================================
#  LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================================================
#  USUARIO AUTENTICADO (PAYLOAD)
# ============================================================

class AuthUser(BaseModel):
    id: int
    nombre: str
    email: EmailStr

    # Roles del usuario autenticado
    roles: List[RolResponse]

    # Permisos efectivos (calculados por get_current_user)
    permisos: Optional[List[str]] = None

    @classmethod
    def model_validate(cls, user):
        """
        Construcción manual desde el modelo SQLAlchemy Usuario.
        """
        return cls(
            id=user.id,
            nombre=user.nombre,
            email=user.email,
            roles=[ur.rol for ur in user.roles_relacion],
            permisos=list(user.permisos) if hasattr(user, "permisos") else None
        )

    class Config:
        from_attributes = True


# ============================================================
#  LOGIN RESPONSE
# ============================================================

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: AuthUser
    refresh_token: Optional[str] = None

    class Config:
        from_attributes = True
