# ============================================================
#  ROUTER: API (TEST_API)
# ============================================================

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.my_api import (
    get_api,
    get_apis,
    create_api,
    update_api,
    delete_api,
    get_parametros_de_api,
    test_api_call,
)
from schemas.my_api import (
    ApiCreate,
    ApiUpdate,
    ApiResponse,
    ApiTestRequest,
    ApiTestResponse,
)
from schemas.objeto_parametro import ObjetoParametroResponse

from core.permissions import require_permission

router = APIRouter(prefix="/apis", tags=["API"])


# -----------------------------
# Listar todas las APIs
# -----------------------------
@router.get(
    "/",
    response_model=list[ApiResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_ver"))]
)
def listar_apis(db: Session = Depends(get_db)):
    return get_apis(db)


# -----------------------------
# Obtener API por ID
# -----------------------------
@router.get(
    "/{api_id}",
    response_model=ApiResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_ver"))]
)
def obtener_api(api_id: int, db: Session = Depends(get_db)):
    return get_api(db, api_id)


# -----------------------------
# Crear API
# -----------------------------
@router.post(
    "/",
    response_model=ApiResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_crear"))]
)
def crear_api(data: ApiCreate, db: Session = Depends(get_db)):
    return create_api(db, data)


# -----------------------------
# Actualizar API
# -----------------------------
@router.put(
    "/{api_id}",
    response_model=ApiResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_editar"))]
)
def actualizar_api(api_id: int, data: ApiUpdate, db: Session = Depends(get_db)):
    return update_api(db, api_id, data)


# -----------------------------
# Eliminar API
# -----------------------------
@router.delete(
    "/{api_id}",
    status_code=204,
    dependencies=[Depends(require_permission("api_eliminar"))]
)
def eliminar_api(api_id: int, db: Session = Depends(get_db)):
    delete_api(db, api_id)
    return Response(status_code=204)


# -----------------------------
# Listar parámetros asociados a una API
# -----------------------------
@router.get(
    "/{api_id}/parametros",
    response_model=list[ObjetoParametroResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_ver"))]
)
def listar_parametros_de_api(api_id: int, db: Session = Depends(get_db)):
    return get_parametros_de_api(db, api_id)


# -----------------------------
# Test de API
# -----------------------------
@router.post(
    "/test",
    response_model=ApiTestResponse,
    dependencies=[Depends(require_permission("api_probar"))]
)
def probar_api(data: ApiTestRequest):
    return test_api_call(data)
