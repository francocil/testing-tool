from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional


# ------------------------------------------------------------
#  VALIDACIÓN DE DNI (algoritmo institucional básico)
# ------------------------------------------------------------
def validar_dni_basico(dni: str) -> bool:
    if not dni.isdigit():
        return False
    if len(dni) not in (7, 8):
        return False
    if dni.startswith("0"):
        return False
    numero = int(dni)
    return 1_000_000 <= numero <= 99_999_999


# ------------------------------------------------------------
#  VALIDACIÓN DE CUIL (estructura simple + prefijo)
# ------------------------------------------------------------
def validar_cuil_basico(cuil: str) -> bool:
    cuil = cuil.replace("-", "").strip()
    if not cuil.isdigit():
        return False
    if len(cuil) != 11:
        return False
    prefijo = cuil[:2]
    if prefijo not in ("20", "27", "23", "24", "30"):
        return False
    return True


def genero_por_cuil(cuil: str) -> Optional[str]:
    if not cuil:
        return None
    limpio = cuil.replace("-", "").strip()
    if len(limpio) != 11:
        return None
    prefijo = limpio[:2]
    if prefijo == "20":
        return "masculino"
    if prefijo == "27":
        return "femenino"
    return None


# ------------------------------------------------------------
#  BASE
# ------------------------------------------------------------
class AgenteBase(BaseModel):
    dni: str
    cuil: str
    apellido_nombre: str
    email: EmailStr

    reparticion_id: int
    direccion_id: int
    area_id: int
    cargo: str

    genero: Optional[str] = None
    activo: bool = True

    @validator("dni")
    def validar_dni(cls, v):
        if not validar_dni_basico(v):
            raise ValueError("DNI inválido")
        return v

    @validator("cuil")
    def validar_cuil(cls, v):
        if not validar_cuil_basico(v):
            raise ValueError("CUIL inválido")
        return v

    @validator("genero", always=True)
    def calcular_genero(cls, v, values):
        cuil = values.get("cuil")
        genero = genero_por_cuil(cuil) if cuil else None
        return genero


# ------------------------------------------------------------
#  CREATE
# ------------------------------------------------------------
class AgenteCreate(AgenteBase):
    pass


# ------------------------------------------------------------
#  UPDATE
# ------------------------------------------------------------
class AgenteUpdate(BaseModel):
    dni: Optional[str] = None
    cuil: Optional[str] = None
    apellido_nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    genero: Optional[str] = None
    activo: Optional[bool] = None

    @validator("dni")
    def validar_dni_update(cls, v):
        if v is not None and not validar_dni_basico(v):
            raise ValueError("DNI inválido")
        return v

    @validator("cuil")
    def validar_cuil_update(cls, v):
        if v is not None and not validar_cuil_basico(v):
            raise ValueError("CUIL inválido")
        return v

    @validator("genero", always=True)
    def calcular_genero_update(cls, v, values):
        cuil = values.get("cuil")
        genero = genero_por_cuil(cuil) if cuil else None
        return genero or v


# ------------------------------------------------------------
#  RESPONSE
# ------------------------------------------------------------
class AgenteOut(AgenteBase):
    id: int
    fecha_creacion: datetime
    fecha_baja: Optional[datetime] = None

    creado_por_usuario_id: Optional[int] = None
    modificado_por_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True
