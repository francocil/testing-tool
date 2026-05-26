from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.direccion import Direccion
from models.reparticion import Reparticion
from schemas.direccion import DireccionCreate, DireccionUpdate


# -----------------------------
# Obtener todas las direcciones
# -----------------------------
def get_direcciones(db: Session, reparticion_id: int | None = None):
    query = db.query(Direccion).order_by(Direccion.nombre)

    if reparticion_id is not None:
        query = query.filter(Direccion.reparticion_id == reparticion_id)

    return query.all()


# -----------------------------
# Obtener dirección por ID
# -----------------------------
def get_direccion(db: Session, direccion_id: int):
    direccion = (
        db.query(Direccion)
        .filter(Direccion.id == direccion_id)
        .first()
    )

    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )

    return direccion


# -----------------------------
# Crear dirección
# -----------------------------
def create_direccion(db: Session, data: DireccionCreate):
    # Validar que exista la repartición
    reparticion = (
        db.query(Reparticion)
        .filter(Reparticion.id == data.reparticion_id)
        .first()
    )

    if not reparticion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repartición no encontrada"
        )

    nueva = Direccion(**data.dict())

    db.add(nueva)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ya existe una dirección con ese nombre en esta repartición"
        )

    db.refresh(nueva)
    return nueva


# -----------------------------
# Actualizar dirección
# -----------------------------
def update_direccion(db: Session, direccion_id: int, data: DireccionUpdate):
    direccion = get_direccion(db, direccion_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(direccion, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ya existe una dirección con ese nombre en esta repartición"
        )

    db.refresh(direccion)
    return direccion


# -----------------------------
# Eliminar dirección
# -----------------------------
def delete_direccion(db: Session, direccion_id: int):
    direccion = get_direccion(db, direccion_id)
    db.delete(direccion)
    db.commit()
