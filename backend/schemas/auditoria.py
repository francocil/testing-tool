from pydantic import BaseModel
from datetime import datetime

class AuditoriaBase(BaseModel):
    usuario_id: int | None = None
    accion: str
    ip: str | None = None
    user_agent: str | None = None

class AuditoriaCreate(AuditoriaBase):
    pass

class AuditoriaOut(AuditoriaBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True
