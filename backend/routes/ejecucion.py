from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.ejecucion import (
    get_ejecucion,
    list_ejecuciones,
    create_ejecucion,
    update_ejecucion,
    delete_ejecucion,
)
from services.motor_ejecucion import (
    ejecutar_ejecucion,
    ejecutar_siguiente_paso,
    registrar_paso_manual
)
from schemas.ejecucion import (
    EjecucionCreate,
    EjecucionUpdate,
    Ejecucion,
)

from core.permissions import require_permission


router = APIRouter(prefix="/ejecuciones", tags=["Ejecuciones"])


# ============================================================
# LISTAR EJECUCIONES
# ============================================================
@router.get(
    "/",
    response_model=list[Ejecucion],
    dependencies=[Depends(require_permission("ejecucion_ver_todos"))]
)
def listar_ejecuciones(db: Session = Depends(get_db)):
    return list_ejecuciones(db)


@router.get(
    "/by-caso/{caso_id}",
    response_model=list[Ejecucion],
    dependencies=[Depends(require_permission("ejecucion_ver_todos"))]
)
def listar_ejecuciones_por_caso(caso_id: int, db: Session = Depends(get_db)):
    return list_ejecuciones(db, caso_id)


# ============================================================
# OBTENER EJECUCIÓN POR ID
# ============================================================
@router.get(
    "/{ejecucion_id}",
    response_model=Ejecucion,
    dependencies=[Depends(require_permission("ejecucion_ver_todos"))]
)
def obtener_ejecucion(ejecucion_id: int, db: Session = Depends(get_db)):
    return get_ejecucion(db, ejecucion_id)


# ============================================================
# CREAR EJECUCIÓN
# ============================================================
@router.post(
    "/",
    response_model=Ejecucion,
    status_code=201,
    dependencies=[Depends(require_permission("ejecucion_crear"))]
)
def crear_ejecucion_endpoint(data: EjecucionCreate, db: Session = Depends(get_db)):
    return create_ejecucion(db, data)


# ============================================================
# ACTUALIZAR EJECUCIÓN
# ============================================================
@router.put(
    "/{ejecucion_id}",
    response_model=Ejecucion,
    dependencies=[Depends(require_permission("ejecucion_editar"))]
)
def actualizar_ejecucion_endpoint(ejecucion_id: int, data: EjecucionUpdate, db: Session = Depends(get_db)):
    return update_ejecucion(db, ejecucion_id, data)


# ============================================================
# ELIMINAR EJECUCIÓN
# ============================================================
@router.delete(
    "/{ejecucion_id}",
    status_code=204,
    dependencies=[Depends(require_permission("ejecucion_eliminar"))]
)
def eliminar_ejecucion_endpoint(ejecucion_id: int, db: Session = Depends(get_db)):
    delete_ejecucion(db, ejecucion_id)
    return Response(status_code=204)


# ============================================================
# EJECUTAR EJECUCIÓN COMPLETA
# ============================================================
@router.post(
    "/{ejecucion_id}/ejecutar",
    response_model=Ejecucion,
    dependencies=[Depends(require_permission("ejecucion_ejecutar"))]
)
def ejecutar_ejecucion_endpoint(ejecucion_id: int, db: Session = Depends(get_db)):
    return ejecutar_ejecucion(db, ejecucion_id)


# ============================================================
# EJECUTAR SIGUIENTE PASO
# ============================================================
@router.post(
    "/{ejecucion_id}/siguiente-paso",
    response_model=Ejecucion,
    dependencies=[Depends(require_permission("ejecucion_ejecutar"))]
)
def ejecutar_siguiente_paso_endpoint(ejecucion_id: int, db: Session = Depends(get_db)):
    return ejecutar_siguiente_paso(db, ejecucion_id)


# ============================================================
# REGISTRAR PASO MANUAL
# ============================================================
@router.post(
    "/{ejecucion_id}/pasos/{paso_id}/manual",
    response_model=Ejecucion,
    dependencies=[Depends(require_permission("ejecucion_registrar_manual"))]
)
def registrar_paso_manual_endpoint(ejecucion_id: int, paso_id: int, estado: str, resultado: str, db: Session = Depends(get_db)):
    registrar_paso_manual(db, ejecucion_id, paso_id, estado, resultado)
    return get_ejecucion(db, ejecucion_id)
