from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Base
# -----------------------------
class CasoPruebaVersionBase(BaseModel):
    caso_id: int
    nro_version: int
    objetivo: Optional[str] = None
    porcentaje_aceptacion: Optional[float] = None


# -----------------------------
# Create
# -----------------------------
class CasoPruebaVersionCreate(CasoPruebaVersionBase):
    pass


# -----------------------------
# Update
# -----------------------------
class CasoPruebaVersionUpdate(BaseModel):
    objetivo: Optional[str] = None
    porcentaje_aceptacion: Optional[float] = None


# -----------------------------
# Response
# -----------------------------
class CasoPruebaVersionResponse(CasoPruebaVersionBase):
    id: int
    fecha: datetime

    model_config = {
        "from_attributes": True
    }
