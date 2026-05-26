from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session, joinedload

from db.session import get_db
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)
from core.auth import get_current_user

from schemas.auth import LoginRequest, LoginResponse, AuthUser
from schemas.usuario import UsuarioResponse
from models.usuario import Usuario
from models.usuario_rol import UsuarioRol
from models.rol import Rol

# Auditoría
from services.auditoria import registrar_evento
from schemas.auditoria import AuditoriaCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_client_info(request: Request):
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")
    return ip, user_agent


@router.post("/login", response_model=LoginResponse)
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    ip, user_agent = get_client_info(request)

    user = (
        db.query(Usuario)
        .options(
            joinedload(Usuario.roles_relacion)
            .joinedload(UsuarioRol.rol)
            .joinedload(Rol.permisos_relacion)
        )
        .filter(Usuario.email == payload.email)
        .first()
    )

    if not user or not verify_password(payload.password, user.password_hash):
        registrar_evento(
            db,
            AuditoriaCreate(
                usuario_id=None,
                accion="login_failed",
                ip=ip,
                user_agent=user_agent
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # ============================================================
    # PERMISOS EFECTIVOS DEL USUARIO
    # ============================================================
    permisos = {
        rp.permiso.nombre
        for ur in user.roles_relacion
        for rp in ur.rol.permisos_relacion
    }

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    registrar_evento(
        db,
        AuditoriaCreate(
            usuario_id=user.id,
            accion="login",
            ip=ip,
            user_agent=user_agent
        )
    )

    # ============================================================
    # RESPUESTA FINAL
    # ============================================================
    usuario_data = AuthUser.model_validate(user)
    usuario_data.permisos = list(permisos)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        usuario=usuario_data
    )


@router.post("/refresh")
def refresh_token(refresh_token: str, request: Request, db: Session = Depends(get_db)):
    ip, user_agent = get_client_info(request)

    payload = decode_refresh_token(refresh_token)

    if not payload:
        registrar_evento(
            db,
            AuditoriaCreate(
                usuario_id=None,
                accion="refresh_failed",
                ip=ip,
                user_agent=user_agent
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado"
        )

    user_id = payload.get("sub")

    if not user_id:
        registrar_evento(
            db,
            AuditoriaCreate(
                usuario_id=None,
                accion="refresh_failed",
                ip=ip,
                user_agent=user_agent
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()

    if not user:
        registrar_evento(
            db,
            AuditoriaCreate(
                usuario_id=None,
                accion="refresh_failed",
                ip=ip,
                user_agent=user_agent
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    new_access_token = create_access_token({"sub": str(user.id)})

    registrar_evento(
        db,
        AuditoriaCreate(
            usuario_id=user.id,
            accion="refresh",
            ip=ip,
            user_agent=user_agent
        )
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UsuarioResponse,
    response_model_exclude_none=True
)
def obtener_usuario_actual(
    current_user = Depends(get_current_user),
):
    roles = [
        {
            "id": ur.rol.id,
            "nombre": ur.rol.nombre
        }
        for ur in current_user.roles_relacion
    ]

    permisos = list(current_user.permisos)

    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "activo": current_user.activo,
        "fecha_creacion": current_user.fecha_creacion,
        "fecha_actualizacion": current_user.fecha_actualizacion,
        "roles": roles,
        "permisos": permisos
    }
