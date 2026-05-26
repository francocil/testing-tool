from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload

from db.session import get_db
from core.security import decode_access_token
from models.usuario import Usuario
from models.usuario_rol import UsuarioRol
from models.rol import Rol
from models.rol_permiso import RolPermiso
from models.permiso import Permiso

"""
Responsabilidades de este módulo:
1- Validar tokens de acceso (JWT)
2- Obtener el usuario actual desde el token
3- Verificar roles (require_role)
4- (Opcional) adjuntar permisos efectivos al usuario en memoria
"""

# -----------------------------
#  CONSTANTES DE ROLES
# -----------------------------
ROL_ADMIN = 1
ROL_TESTER = 2
ROL_VISOR = 3

# -----------------------------
#  ESQUEMA DE AUTORIZACIÓN (BEARER TOKEN)
# -----------------------------
# auto_error=False evita que el esquema lance 403 antes de tiempo
bearer_scheme = HTTPBearer(auto_error=False)


# ============================================================
#  RESOLVER PERMISOS DEL USUARIO (INTERNO)
#  Cadena:
#     Usuario → UsuarioRol → Rol → RolPermiso → Permiso
# ============================================================
def _resolve_permissions(db: Session, usuario: Usuario) -> set[str]:
    """
    Devuelve el conjunto de permisos efectivos del usuario.
    """

    usuario_db: Usuario | None = (
        db.query(Usuario)
        .options(
            joinedload(Usuario.roles_relacion)
            .joinedload(UsuarioRol.rol)
            .joinedload(Rol.permisos_relacion)
            .joinedload(RolPermiso.permiso)
        )
        .filter(Usuario.id == usuario.id)
        .first()
    )

    if not usuario_db:
        return set()

    permisos: set[str] = set()

    for usuario_rol in usuario_db.roles_relacion:
        rol = usuario_rol.rol
        if not rol:
            continue

        for rol_permiso in rol.permisos_relacion:
            permiso = rol_permiso.permiso
            if permiso and permiso.activo:
                permisos.add(permiso.nombre)

    return permisos


# -----------------------------
#  USUARIO ACTUAL (EXTENDIDO)
# -----------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtiene el usuario autenticado desde el token.
    Además:
    - Carga roles del usuario
    - Carga permisos dinámicos del usuario (en user.permisos)
    """

    # Si no hay credenciales, devolvemos 401 explícito
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autenticación"
        )

    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = (
        db.query(Usuario)
        .options(
            joinedload(Usuario.roles_relacion)
            .joinedload(UsuarioRol.rol)
        )
        .filter(Usuario.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    # Adjuntar permisos efectivos en memoria (no se persiste)
    user.permisos = _resolve_permissions(db, user)

    return user


# -----------------------------
#  PERMISOS POR ROL
# -----------------------------
def require_role(*allowed_roles: int):
    """
    Verifica que el usuario tenga al menos uno de los roles indicados.
    Compatible con el modelo Usuario → UsuarioRol → Rol.
    """
    def role_checker(
        user: Usuario = Depends(get_current_user),
    ):
        roles_usuario = {ur.rol_id for ur in user.roles_relacion}

        if not any(r in roles_usuario for r in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para realizar esta acción"
            )

        return user

    return role_checker
