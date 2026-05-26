# ============================================================
#  ROUTER: API_VERSION
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from core.permissions import require_permission

from services.api_version import (
    get_versiones_de_api,
    get_version,
    crear_version_desde_api,
    crear_version_manual,
    rollback_version,
    clonar_version,
)

from schemas.api_version import ApiVersionResponse, ApiVersionCreate

router = APIRouter(prefix="/apis/versiones", tags=["API Versiones"])


# -----------------------------
# Listar versiones de una API
# -----------------------------
@router.get(
    "/by-api/{api_id}",
    response_model=list[ApiVersionResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_versionar"))]
)
def listar_versiones(api_id: int, db: Session = Depends(get_db)):
    return get_versiones_de_api(db, api_id)


# -----------------------------
# Obtener una versión específica
# -----------------------------
@router.get(
    "/{version_id}",
    response_model=ApiVersionResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_versionar"))]
)
def obtener_version(version_id: int, db: Session = Depends(get_db)):
    return get_version(db, version_id)


# -----------------------------
# Crear versión desde API actual
# -----------------------------
@router.post(
    "/crear-desde-api/{api_id}",
    response_model=ApiVersionResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_versionar"))]
)
def versionar_api(api_id: int, db: Session = Depends(get_db)):
    usuario_id = None
    return crear_version_desde_api(db, api_id, usuario_id)


# -----------------------------
# Crear versión manual
# -----------------------------
@router.post(
    "/",
    response_model=ApiVersionResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("api_versionar"))]
)
def crear_version(data: ApiVersionCreate, db: Session = Depends(get_db)):
    return crear_version_manual(db, data)


# -----------------------------
# Rollback
# -----------------------------
@router.post(
    "/rollback/{version_id}",
    dependencies=[Depends(require_permission("api_versionar"))]
)
def rollback_version_endpoint(version_id: int, db: Session = Depends(get_db)):
    return rollback_version(db, version_id)


# -----------------------------
# Clonar versión
# -----------------------------
@router.post(
    "/clonar/{version_id}",
    dependencies=[Depends(require_permission("api_versionar"))]
)
def clonar_version_endpoint(version_id: int, db: Session = Depends(get_db)):
    return clonar_version(db, version_id)


# -----------------------------
# Exportar versión
# -----------------------------
@router.get(
    "/exportar/{version_id}",
    dependencies=[Depends(require_permission("api_versionar"))]
)
def exportar_version(version_id: int, db: Session = Depends(get_db)):
    version = get_version(db, version_id)

    data = {
        "id": version.id,
        "api_id": version.api_id,
        "version": version.version,
        "metodo": version.metodo,
        "base_url": version.base_url,
        "endpoint": version.endpoint,
        "auth_tipo": version.auth_tipo,
        "auth_config": version.auth_config,
        "headers_por_defecto": version.headers_por_defecto,
        "body_ejemplo": version.body_ejemplo,
        "timeout_segundos": version.timeout_segundos,
        "retries": version.retries,
        "fecha_creacion": str(version.fecha_creacion),
    }

    from fastapi.responses import JSONResponse

    response = JSONResponse(content=data)
    response.headers["Content-Disposition"] = (
        f"attachment; filename=api_version_{version.id}.json"
    )
    return response
