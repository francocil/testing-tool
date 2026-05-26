from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models.reparticion import Reparticion
from schemas.reparticion import ReparticionCreate, ReparticionUpdate


def get_reparticiones(db: Session):
    return db.query(Reparticion).order_by(Reparticion.nombre).all()


def get_reparticion(db: Session, id: int):
    rep = db.query(Reparticion).filter(Reparticion.id == id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Repartición no encontrada")
    return rep


def create_reparticion(db: Session, data: ReparticionCreate):
    nueva = Reparticion(**data.dict())
    db.add(nueva)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")

    db.refresh(nueva)
    return nueva


def update_reparticion(db: Session, id: int, data: ReparticionUpdate):
    rep = get_reparticion(db, id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(rep, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")

    db.refresh(rep)
    return rep


def delete_reparticion(db: Session, id: int):
    rep = get_reparticion(db, id)
    db.delete(rep)
    db.commit()
