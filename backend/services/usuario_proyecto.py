from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.usuario_proyecto import UsuarioProyecto
from models.usuario import Usuario
from models.proyecto import Proyecto
from schemas.usuario_proyecto import UsuarioProyectoCreate, UsuarioProyectoUpdate


# -----------------------------
# Listar asignaciones usuario-proyecto
# -----------------------------
def get_usuario_proyectos(db: Session) -> list[UsuarioProyecto]:
    return db.query(UsuarioProyecto).all()


# -----------------------------
# Obtener asignación por ID
# -----------------------------
def get_usuario_proyecto(db: Session, asignacion_id: int) -> UsuarioProyecto:
    asignacion = (
        db.query(UsuarioProyecto)
        .filter(UsuarioProyecto.id == asignacion_id)
        .first()
    )

    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación usuario-proyecto no encontrada"
        )

    return asignacion


# -----------------------------
# Crear asignación usuario-proyecto
# -----------------------------
def create_usuario_proyecto(db: Session, data: UsuarioProyectoCreate) -> UsuarioProyecto:
    # Validar existencia de usuario
    usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Validar existencia de proyecto
    proyecto = db.query(Proyecto).filter(Proyecto.id == data.proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )

    # Validar duplicado usuario-proyecto
    existente = (
        db.query(UsuarioProyecto)
        .filter(
            UsuarioProyecto.usuario_id == data.usuario_id,
            UsuarioProyecto.proyecto_id == data.proyecto_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya está asignado a este proyecto"
        )

    nueva = UsuarioProyecto(
        usuario_id=data.usuario_id,
        proyecto_id=data.proyecto_id
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# -----------------------------
# Actualizar asignación usuario-proyecto
# -----------------------------
def update_usuario_proyecto(db: Session, asignacion_id: int, data: UsuarioProyectoUpdate) -> UsuarioProyecto:
    asignacion = get_usuario_proyecto(db, asignacion_id)

    nuevo_usuario_id = data.usuario_id if data.usuario_id is not None else asignacion.usuario_id
    nuevo_proyecto_id = data.proyecto_id if data.proyecto_id is not None else asignacion.proyecto_id

    # Validar existencia de usuario si cambia
    if data.usuario_id is not None:
        usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

    # Validar existencia de proyecto si cambia
    if data.proyecto_id is not None:
        proyecto = db.query(Proyecto).filter(Proyecto.id == data.proyecto_id).first()
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )

    # Validar duplicado usuario-proyecto
    existente = (
        db.query(UsuarioProyecto)
        .filter(
            UsuarioProyecto.usuario_id == nuevo_usuario_id,
            UsuarioProyecto.proyecto_id == nuevo_proyecto_id,
            UsuarioProyecto.id != asignacion_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe otra asignación con este usuario y proyecto"
        )

    asignacion.usuario_id = nuevo_usuario_id
    asignacion.proyecto_id = nuevo_proyecto_id

    db.commit()
    db.refresh(asignacion)
    return asignacion


# -----------------------------
# Eliminar asignación usuario-proyecto
# -----------------------------
def delete_usuario_proyecto(db: Session, asignacion_id: int) -> None:
    asignacion = get_usuario_proyecto(db, asignacion_id)
    db.delete(asignacion)
    db.commit()
