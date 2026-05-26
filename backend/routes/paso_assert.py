# ============================================================
#  ROUTES: PasoAssert
# ------------------------------------------------------------
#  Endpoints para gestionar asserts asociados a un paso.
# ============================================================

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from core.deps import get_db
from core.permissions import require_permission

from schemas.paso_assert import (
    PasoAssertCreate,
    PasoAssertUpdate,
    PasoAssertResponse
)

from services.paso_assert import (
    list_asserts_by_paso,
    create_assert,
    update_assert,
    delete_assert
)

router = APIRouter(prefix="/paso-assert", tags=["PasoAssert"])


# ------------------------------------------------------------
# Listar asserts de un paso
# ------------------------------------------------------------
@router.get(
    "/by-paso/{paso_id}",
    response_model=list[PasoAssertResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_parametros"))]
)
def listar_asserts_por_paso(paso_id: int, db: Session = Depends(get_db)):
    """
    Devuelve todos los asserts asociados a un paso.
    """
    return list_asserts_by_paso(db, paso_id)


# ------------------------------------------------------------
# Crear assert
# ------------------------------------------------------------
@router.post(
    "/",
    response_model=PasoAssertResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_parametros"))]
)
def crear_assert_endpoint(data: PasoAssertCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo assert para un paso.
    """
    return create_assert(db, data.paso_id, data)


# ------------------------------------------------------------
# Actualizar assert
# ------------------------------------------------------------
@router.put(
    "/{assert_id}",
    response_model=PasoAssertResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_parametros"))]
)
def actualizar_assert_endpoint(assert_id: int, data: PasoAssertUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un assert existente.
    """
    return update_assert(db, assert_id, data)


# ------------------------------------------------------------
# Eliminar assert
# ------------------------------------------------------------
@router.delete(
    "/{assert_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_parametros"))]
)
def eliminar_assert_endpoint(assert_id: int, db: Session = Depends(get_db)):
    """
    Elimina un assert asociado a un paso.
    """
    delete_assert(db, assert_id)
    return Response(status_code=204)
