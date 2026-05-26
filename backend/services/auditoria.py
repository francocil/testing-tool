from sqlalchemy.orm import Session
from models.auditoria import Auditoria
from schemas.auditoria import AuditoriaCreate

def registrar_evento(db: Session, data: AuditoriaCreate):
    evento = Auditoria(**data.dict())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def listar_eventos(db: Session, usuario_id: int | None = None):
    query = db.query(Auditoria).order_by(Auditoria.fecha.desc())
    if usuario_id:
        query = query.filter(Auditoria.usuario_id == usuario_id)
    return query.all()
