from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .objeto_parametro import ObjetoParametroResponse


# ============================================================
#  BASE
# ============================================================

class ApiBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    metodo: str
    base_url: Optional[str] = None
    endpoint: str
    auth_tipo: str = "none"
    auth_config: Optional[Dict[str, Any]] = None
    headers_por_defecto: Optional[Dict[str, Any]] = None
    body_ejemplo: Optional[Dict[str, Any]] = None
    timeout_segundos: int = 10
    retries: int = 0
    version: str = "v1"
    activo: bool = True


# ============================================================
#  CREATE
# ============================================================

class ApiCreate(ApiBase):
    pass


# ============================================================
#  UPDATE
# ============================================================

class ApiUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    metodo: Optional[str] = None
    base_url: Optional[str] = None
    endpoint: Optional[str] = None
    auth_tipo: Optional[str] = None
    auth_config: Optional[Dict[str, Any]] = None
    headers_por_defecto: Optional[Dict[str, Any]] = None
    body_ejemplo: Optional[Dict[str, Any]] = None
    timeout_segundos: Optional[int] = None
    retries: Optional[int] = None
    version: Optional[str] = None
    activo: Optional[bool] = None


# ============================================================
#  RESPONSE
# ============================================================

class ApiResponse(ApiBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    parametros: List[ObjetoParametroResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


# ============================================================
#  TEST REQUEST / RESPONSE
# ============================================================

class ApiTestRequest(BaseModel):
    metodo: str
    base_url: str
    endpoint: str
    headers: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 10


class ApiTestResponse(BaseModel):
    status_code: int
    headers: Dict[str, Any]
    body: Any
    ok: bool
    elapsed_ms: int
