from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.rol import Rol
from schemas.rol import RolCreate, RolUpdate


# -----------------------------
# Listar roles
# -----------------------------
def get_roles(db: Session) -> list[Rol]:
    return db.query(Rol).all()


# -----------------------------
# Obtener rol por ID
# -----------------------------
def get_rol(db: Session, rol_id: int) -> Rol:
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol


# -----------------------------
# Crear rol
# -----------------------------
def create_rol(db: Session, data: RolCreate) -> Rol:
    existente = db.query(Rol).filter(Rol.nombre == data.nombre).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un rol con ese nombre"
        )

    nuevo = Rol(nombre=data.nombre)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# -----------------------------
# Actualizar rol
# -----------------------------
def update_rol(db: Session, rol_id: int, data: RolUpdate) -> Rol:
    rol = get_rol(db, rol_id)

    if data.nombre is not None and data.nombre != rol.nombre:
        existente = db.query(Rol).filter(Rol.nombre == data.nombre).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe otro rol con ese nombre"
            )
        rol.nombre = data.nombre

    db.commit()
    db.refresh(rol)
    return rol


# -----------------------------
# Eliminar rol
# -----------------------------
def delete_rol(db: Session, rol_id: int) -> None:
    rol = get_rol(db, rol_id)
    db.delete(rol)
    db.commit()
