from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from models.comentario import Comentario, EntidadTipo
from models.usuario import Usuario
from models.ejecucion import Ejecucion
from schemas.comentario import ComentarioCreate, ComentarioUpdate


# -----------------------------
# Obtener comentario por ID
# -----------------------------
def get_comentario(db: Session, comentario_id: int) -> Comentario:
    comentario = (
        db.query(Comentario)
        .options(
            joinedload(Comentario.usuario),
            joinedload(Comentario.ejecucion),
        )
        .filter(Comentario.id == comentario_id)
        .first()
    )

    if not comentario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )

    return comentario


# -----------------------------
# Listar comentarios por entidad
# -----------------------------
def get_comentarios_por_entidad(
    db: Session,
    entidad_tipo: EntidadTipo,
    entidad_id: int
) -> list[Comentario]:

    return (
        db.query(Comentario)
        .options(joinedload(Comentario.usuario))
        .filter(
            Comentario.entidad_tipo == entidad_tipo,
            Comentario.entidad_id == entidad_id
        )
        .all()
    )


# -----------------------------
# Crear comentario
# -----------------------------
def create_comentario(db: Session, data: ComentarioCreate) -> Comentario:
    usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if data.ejecucion_id is not None:
        ejecucion = db.query(Ejecucion).filter(Ejecucion.id == data.ejecucion_id).first()
        if not ejecucion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejecución no encontrada")

    nuevo = Comentario(
        usuario_id=data.usuario_id,
        entidad_tipo=data.entidad_tipo,
        entidad_id=data.entidad_id,
        comentario=data.comentario,
        ejecucion_id=data.ejecucion_id
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# -----------------------------
# Actualizar comentario
# -----------------------------
def update_comentario(db: Session, comentario_id: int, data: ComentarioUpdate) -> Comentario:
    comentario = get_comentario(db, comentario_id)

    if data.comentario is not None:
        comentario.comentario = data.comentario

    db.commit()
    db.refresh(comentario)
    return comentario


# -----------------------------
# Eliminar comentario
# -----------------------------
def delete_comentario(db: Session, comentario_id: int) -> None:
    comentario = get_comentario(db, comentario_id)
    db.delete(comentario)
    db.commit()
