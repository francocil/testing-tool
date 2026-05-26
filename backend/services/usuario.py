from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from core.security import hash_password


# -----------------------------
# Listar usuarios
# -----------------------------
def get_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


# -----------------------------
# Obtener usuario por ID
# -----------------------------
def get_usuario(db: Session, usuario_id: int) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


# -----------------------------
# Crear usuario
# -----------------------------
def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email"
        )

    nuevo = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
        activo=True,
        agente_id=data.agente_id
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# -----------------------------
# Actualizar usuario
# -----------------------------
def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) -> Usuario:
    usuario = get_usuario(db, usuario_id)

    # Validar email duplicado
    if data.email is not None and data.email != usuario.email:
        existente = db.query(Usuario).filter(Usuario.email == data.email).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe otro usuario con ese email"
            )
        usuario.email = data.email

    # Actualizar nombre
    if data.nombre is not None:
        usuario.nombre = data.nombre

    # Actualizar contraseña
    if data.password is not None:
        usuario.password_hash = hash_password(data.password)

    # Actualizar estado activo/inactivo
    if data.activo is not None:
        usuario.activo = data.activo

    # Actualizar agente
    if data.agente_id is not None:
        usuario.agente_id = data.agente_id

    db.commit()
    db.refresh(usuario)
    return usuario


# -----------------------------
# Eliminar usuario
# -----------------------------
def delete_usuario(db: Session, usuario_id: int) -> None:
    usuario = get_usuario(db, usuario_id)
    db.delete(usuario)
    db.commit()
