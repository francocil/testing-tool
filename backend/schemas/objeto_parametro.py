from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
#  BASE
# ============================================================

class ObjetoParametroBase(BaseModel):
    paso_id: int
    api_id: Optional[int] = None
    tipo: str
    nombre: str
    valor_entrada: Optional[str] = None
    valor_esperado: Optional[str] = None


# ============================================================
#  CREATE
# ============================================================

class ObjetoParametroCreate(ObjetoParametroBase):
    """
    No agregamos nada porque todos los campos obligatorios
    ya están definidos en ObjetoParametroBase.
    """
    pass


# ============================================================
#  UPDATE
# ============================================================

class ObjetoParametroUpdate(BaseModel):
    paso_id: Optional[int] = None
    api_id: Optional[int] = None
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    valor_entrada: Optional[str] = None
    valor_esperado: Optional[str] = None


# ============================================================
#  RESPONSE
# ============================================================

class ObjetoParametroResponse(ObjetoParametroBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
