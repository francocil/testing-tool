from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    accion = Column(String(100), nullable=False)
    ip = Column(String(50), nullable=True)
    user_agent = Column(String(300), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
