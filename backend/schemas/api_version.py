from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


# ============================================================
#  BASE
# ------------------------------------------------------------
#  Campos comunes para todas las versiones de API.
# ============================================================

class ApiVersionBase(BaseModel):
    version: str
    metodo: str
    base_url: Optional[str] = None
    endpoint: str

    auth_tipo: str = "none"
    auth_config: Optional[Any] = None

    headers_por_defecto: Optional[Any] = None
    body_ejemplo: Optional[Any] = None

    timeout_segundos: int = 10
    retries: int = 0


# ============================================================
#  CREATE
# ------------------------------------------------------------
#  Para crear una nueva versión (copiada desde Api).
# ============================================================

class ApiVersionCreate(ApiVersionBase):
    api_id: int
    creado_por_usuario_id: Optional[int] = None


# ============================================================
#  RESPONSE
# ------------------------------------------------------------
#  Lo que se devuelve al frontend.
# ============================================================

class ApiVersionResponse(ApiVersionBase):
    id: int
    api_id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
