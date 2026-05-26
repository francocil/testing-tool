from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.comentario import EntidadTipo

# -----------------------------
# Base
# -----------------------------
class ComentarioBase(BaseModel):
    usuario_id: int
    entidad_tipo: EntidadTipo
    entidad_id: int
    comentario: str
    ejecucion_id: Optional[int] = None

# -----------------------------
# Create
# -----------------------------
class ComentarioCreate(ComentarioBase):
    pass

# -----------------------------
# Update
# -----------------------------
class ComentarioUpdate(BaseModel):
    comentario: Optional[str] = None

# -----------------------------
# Response
# -----------------------------
class ComentarioResponse(ComentarioBase):
    id: int
    fecha: datetime

    model_config = {
        "from_attributes": True
    }
