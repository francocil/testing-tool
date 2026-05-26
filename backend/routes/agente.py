from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.agente import AgenteCreate, AgenteUpdate, AgenteOut
from services.agente import (
    listar_agentes,
    obtener_agente,
    crear_agente,
    actualizar_agente,
    eliminar_agente,
)

# 🔐 Sistema de permisos institucional
from core.permissions import require_permission, require_any_permission

router = APIRouter(prefix="/agentes", tags=["Agentes"])


# ============================================================
#  LISTAR AGENTES
# ------------------------------------------------------------
# Permisos válidos:
#   - ver_agentes
#   - admin_agentes
# ============================================================
@router.get(
    "/",
    response_model=list[AgenteOut],
    dependencies=[Depends(require_any_permission("ver_agentes", "admin_agentes"))]
)
def listar(db: Session = Depends(get_db)):
    return listar_agentes(db)


# ============================================================
#  OBTENER AGENTE POR ID
# ------------------------------------------------------------
# Permisos válidos:
#   - ver_agentes
#   - admin_agentes
# ============================================================
@router.get(
    "/{agente_id}",
    response_model=AgenteOut,
    dependencies=[Depends(require_any_permission("ver_agentes", "admin_agentes"))]
)
def obtener(agente_id: int, db: Session = Depends(get_db)):
    agente = obtener_agente(db, agente_id)
    if not agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agente


# ============================================================
#  CREAR AGENTE
# ------------------------------------------------------------
# Permisos válidos:
#   - crear_agentes
#   - admin_agentes
# ============================================================
@router.post(
    "/",
    response_model=AgenteOut,
    dependencies=[Depends(require_any_permission("crear_agentes", "admin_agentes"))]
)
def crear(data: AgenteCreate, db: Session = Depends(get_db)):
    return crear_agente(db, data)


# ============================================================
#  ACTUALIZAR AGENTE
# ------------------------------------------------------------
# Permisos válidos:
#   - editar_agentes
#   - admin_agentes
# ============================================================
@router.put(
    "/{agente_id}",
    response_model=AgenteOut,
    dependencies=[Depends(require_any_permission("editar_agentes", "admin_agentes"))]
)
def actualizar(agente_id: int, data: AgenteUpdate, db: Session = Depends(get_db)):
    agente = actualizar_agente(db, agente_id, data)
    if not agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agente


# ============================================================
#  ELIMINAR AGENTE
# ------------------------------------------------------------
# Permisos válidos:
#   - eliminar_agentes
#   - admin_agentes
# ============================================================
@router.delete(
    "/{agente_id}",
    dependencies=[Depends(require_any_permission("eliminar_agentes", "admin_agentes"))]
)
def eliminar(agente_id: int, db: Session = Depends(get_db)):
    ok = eliminar_agente(db, agente_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return {"detail": "Agente eliminado"}
