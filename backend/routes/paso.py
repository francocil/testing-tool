from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.paso import (
    get_pasos_por_caso,
    get_paso,
    create_paso,
    update_paso,
    delete_paso,
)
from schemas.paso import (
    PasoCreate,
    PasoUpdate,
    Paso,
)

from core.permissions import require_permission

router = APIRouter(prefix="/pasos", tags=["Pasos"])


# ============================================================
# LISTAR PASOS
# ============================================================
@router.get(
    "/",
    response_model=list[Paso],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("paso_ver_caso"))]
)
def listar_pasos(caso_id: int | None = None, db: Session = Depends(get_db)):
    if caso_id is None:
        return []
    return get_pasos_por_caso(db, caso_id)


# ============================================================
# OBTENER PASO POR ID
# ============================================================
@router.get(
    "/{paso_id}",
    response_model=Paso,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("paso_ver_caso"))]
)
def obtener_paso(paso_id: int, db: Session = Depends(get_db)):
    return get_paso(db, paso_id)


# ============================================================
# CREAR PASO
# ============================================================
@router.post(
    "/",
    response_model=Paso,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("paso_crear"))]
)
def crear_paso_route(data: PasoCreate, db: Session = Depends(get_db)):
    return create_paso(db, data)


# ============================================================
# ACTUALIZAR PASO
# ============================================================
@router.put(
    "/{paso_id}",
    response_model=Paso,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("paso_editar"))]
)
def actualizar_paso_route(paso_id: int, data: PasoUpdate, db: Session = Depends(get_db)):
    return update_paso(db, paso_id, data)


# ============================================================
# ELIMINAR PASO
# ============================================================
@router.delete(
    "/{paso_id}",
    status_code=204,
    dependencies=[Depends(require_permission("paso_eliminar"))]
)
def eliminar_paso_route(paso_id: int, db: Session = Depends(get_db)):
    delete_paso(db, paso_id)
    return Response(status_code=204)
