from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models.agente import Agente
from schemas.agente import AgenteCreate, AgenteUpdate


def listar_agentes(db: Session):
    return db.query(Agente).order_by(Agente.apellido_nombre).all()


def obtener_agente(db: Session, agente_id: int):
    return db.query(Agente).filter(Agente.id == agente_id).first()


def crear_agente(db: Session, data: AgenteCreate):
    payload = data.dict(exclude={"genero"})

    agente = Agente(**payload)
    db.add(agente)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="DNI o Email ya están registrados"
        )

    db.refresh(agente)
    return agente


def actualizar_agente(db: Session, agente_id: int, data: AgenteUpdate):
    agente = obtener_agente(db, agente_id)
    if not agente:
        return None

    payload = data.dict(exclude_unset=True, exclude={"genero"})

    for field, value in payload.items():
        setattr(agente, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="DNI o Email ya están registrados"
        )

    db.refresh(agente)
    return agente


def eliminar_agente(db: Session, agente_id: int):
    agente = obtener_agente(db, agente_id)
    if not agente:
        return None

    db.delete(agente)
    db.commit()
    return True
