from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Base
# -----------------------------
class PasoDocumentoBase(BaseModel):
    paso_id: int
    archivo_url: str


# -----------------------------
# Create
# -----------------------------
class PasoDocumentoCreate(PasoDocumentoBase):
    pass


# -----------------------------
# Update
# -----------------------------
class PasoDocumentoUpdate(BaseModel):
    archivo_url: Optional[str] = None


# -----------------------------
# Response
# -----------------------------
class PasoDocumentoResponse(PasoDocumentoBase):
    id: int
    fecha_subida: datetime

    model_config = {
        "from_attributes": True
    }
