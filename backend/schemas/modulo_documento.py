from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Base
# -----------------------------
class ModuloDocumentoBase(BaseModel):
    modulo_id: int
    archivo_url: str


# -----------------------------
# Create
# -----------------------------
class ModuloDocumentoCreate(ModuloDocumentoBase):
    pass


# -----------------------------
# Update
# -----------------------------
class ModuloDocumentoUpdate(BaseModel):
    archivo_url: Optional[str] = None


# -----------------------------
# Response
# -----------------------------
class ModuloDocumentoResponse(ModuloDocumentoBase):
    id: int
    fecha_subida: datetime

    model_config = {
        "from_attributes": True
    }
