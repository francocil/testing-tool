"""
Módulo de permisos del sistema.

Responsabilidades:
- Resolver los permisos efectivos de un usuario
- Verificar si un usuario tiene un permiso dado
- Exponer dependencias reutilizables para proteger endpoints:
    - require_permission("permiso_x")
    - require_any_permission("permiso_x", "permiso_y")
"""

from typing import Set, List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from db.session import get_db
from core.auth import get_current_user
from models.usuario import Usuario
from models.usuario_rol import UsuarioRol
from models.rol import Rol
from models.rol_permiso import RolPermiso
from models.permiso import Permiso


# ============================================================
#  RESOLVER PERMISOS DE UN USUARIO
# ------------------------------------------------------------
#  Cadena:
#     Usuario → UsuarioRol → Rol → RolPermiso → Permiso
# ============================================================

def resolve_user_permissions(db: Session, usuario: Usuario) -> Set[str]:
    """
    Devuelve el conjunto de nombres de permisos efectivos
    asociados al usuario.

    Se basa en:
        Usuario → UsuarioRol → Rol → RolPermiso → Permiso
    """

    # Cargamos todo en una sola consulta con joinedload
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

    permisos: Set[str] = set()

    for usuario_rol in usuario_db.roles_relacion:
        rol = usuario_rol.rol
        if not rol:
            continue

        for rol_permiso in rol.permisos_relacion:
            permiso = rol_permiso.permiso
            if permiso and permiso.activo:
                permisos.add(permiso.nombre)

    return permisos


# ============================================================
#  VERIFICAR SI UN USUARIO TIENE UN PERMISO
# ============================================================

def has_permission(db: Session, usuario: Usuario, permiso_requerido: str) -> bool:
    """
    Indica si el usuario tiene el permiso indicado.
    """
    permisos = resolve_user_permissions(db, usuario)
    return permiso_requerido in permisos


def has_any_permission(db: Session, usuario: Usuario, permisos_requeridos: List[str]) -> bool:
    """
    Indica si el usuario tiene al menos uno de los permisos indicados.
    """
    permisos = resolve_user_permissions(db, usuario)
    return any(p in permisos for p in permisos_requeridos)


# ============================================================
#  DEPENDENCIAS PARA ENDPOINTS
# ------------------------------------------------------------
#  Uso típico:
#
#   from core.permissions import require_permission
#
#   @router.post("/algo", dependencies=[Depends(require_permission("crear_proyecto"))])
#   def crear_algo(...):
#       ...
# ============================================================

def require_permission(permiso: str):
    """
    Dependencia que exige que el usuario tenga
    un permiso específico.
    """
    def checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not has_permission(db, current_user, permiso):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tenés el permiso requerido: {permiso}"
            )
        return current_user

    return checker


def require_any_permission(*permisos: str):
    """
    Dependencia que exige que el usuario tenga
    al menos uno de los permisos indicados.
    """
    def checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not has_any_permission(db, current_user, list(permisos)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tenés ninguno de los permisos requeridos: {', '.join(permisos)}"
            )
        return current_user

    return checker
