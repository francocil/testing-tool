from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from models.my_api import Api
from models.objeto_parametro import ObjetoParametro
from models.paso import Paso
from schemas.my_api import ApiCreate, ApiUpdate, ApiTestRequest, ApiTestResponse
import requests
import json
import re

# 🔥 Import para versionado automático
from services.api_version import crear_version_desde_api


# ============================================================
#  VALIDACIONES
# ============================================================

METODOS_VALIDOS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
AUTH_VALIDOS = {"none", "basic", "bearer", "api_key"}


def _validar_metodo(metodo: str):
    if metodo.upper() not in METODOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Método inválido: {metodo}. Permitidos: {', '.join(METODOS_VALIDOS)}"
        )


def _validar_url(url: str | None):
    if not url:
        return
    if not re.match(r"^https?://", url):
        raise HTTPException(status_code=400, detail="base_url debe comenzar con http:// o https://")


def _validar_endpoint(endpoint: str):
    if not endpoint:
        raise HTTPException(status_code=400, detail="endpoint no puede estar vacío")
    if not endpoint.startswith("/"):
        raise HTTPException(status_code=400, detail="endpoint debe comenzar con /")


def _validar_json(valor, nombre: str):
    if valor is None:
        return
    if not isinstance(valor, dict):
        raise HTTPException(status_code=400, detail=f"{nombre} debe ser un objeto JSON válido")


def _validar_auth(auth_tipo: str, auth_config):
    if auth_tipo not in AUTH_VALIDOS:
        raise HTTPException(status_code=400, detail=f"auth_tipo inválido: {auth_tipo}")

    if auth_tipo == "basic":
        if not auth_config or "username" not in auth_config or "password" not in auth_config:
            raise HTTPException(status_code=400, detail="auth_config debe incluir username y password")

    if auth_tipo == "bearer":
        if not auth_config or "token" not in auth_config:
            raise HTTPException(status_code=400, detail="auth_config debe incluir token")

    if auth_tipo == "api_key":
        if not auth_config or "key" not in auth_config or "header" not in auth_config:
            raise HTTPException(status_code=400, detail="auth_config debe incluir key y header")


def _validar_version(version: str):
    if not re.match(r"^v\d+(\.\d+)?$", version):
        raise HTTPException(status_code=400, detail="La versión debe tener formato v1 o v1.1")


def _validar_timeout(timeout: int):
    if timeout < 1 or timeout > 120:
        raise HTTPException(status_code=400, detail="timeout_segundos debe estar entre 1 y 120")


def _validar_retries(retries: int):
    if retries < 0 or retries > 10:
        raise HTTPException(status_code=400, detail="retries debe estar entre 0 y 10")


# ============================================================
#  GETTERS
# ============================================================

def get_parametros_de_api(db: Session, api_id: int):
    return db.query(ObjetoParametro).filter(ObjetoParametro.api_id == api_id).all()


def get_apis(db: Session) -> list[Api]:
    return db.query(Api).options(joinedload(Api.parametros)).all()


def get_api(db: Session, api_id: int) -> Api:
    api = (
        db.query(Api)
        .options(joinedload(Api.parametros))
        .filter(Api.id == api_id)
        .first()
    )

    if not api:
        raise HTTPException(status_code=404, detail="API no encontrada")

    return api


# ============================================================
#  CREAR API
# ============================================================

def create_api(db: Session, data: ApiCreate) -> Api:

    # Validaciones
    _validar_metodo(data.metodo)
    _validar_url(data.base_url)
    _validar_endpoint(data.endpoint)
    _validar_json(data.headers_por_defecto, "headers_por_defecto")
    _validar_json(data.body_ejemplo, "body_ejemplo")
    _validar_auth(data.auth_tipo, data.auth_config)
    _validar_version(data.version)
    _validar_timeout(data.timeout_segundos)
    _validar_retries(data.retries)

    # Nombre único (case-insensitive)
    existente = (
        db.query(Api)
        .filter(Api.nombre.ilike(data.nombre))
        .first()
    )

    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una API con ese nombre")

    nueva = Api(
        nombre=data.nombre.strip(),
        descripcion=data.descripcion,
        metodo=data.metodo.upper(),
        base_url=data.base_url,
        endpoint=data.endpoint,
        auth_tipo=data.auth_tipo,
        auth_config=json.dumps(data.auth_config) if data.auth_config else None,
        headers_por_defecto=json.dumps(data.headers_por_defecto) if data.headers_por_defecto else None,
        body_ejemplo=json.dumps(data.body_ejemplo) if data.body_ejemplo else None,
        timeout_segundos=data.timeout_segundos,
        retries=data.retries,
        version=data.version,
        activo=1 if data.activo else 0,
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # Crear versión inicial
    crear_version_desde_api(db, nueva.id, None)

    return nueva


# ============================================================
#  ACTUALIZAR API
# ============================================================

def update_api(db: Session, api_id: int, data: ApiUpdate) -> Api:
    api = get_api(db, api_id)

    # Guardar versión antes de modificar
    crear_version_desde_api(db, api.id, None)

    # Validaciones
    if data.metodo is not None:
        _validar_metodo(data.metodo)

    if data.base_url is not None:
        _validar_url(data.base_url)

    if data.endpoint is not None:
        _validar_endpoint(data.endpoint)

    if data.headers_por_defecto is not None:
        _validar_json(data.headers_por_defecto, "headers_por_defecto")

    if data.body_ejemplo is not None:
        _validar_json(data.body_ejemplo, "body_ejemplo")

    if data.auth_tipo is not None:
        _validar_auth(data.auth_tipo, data.auth_config)

    if data.version is not None:
        _validar_version(data.version)

    if data.timeout_segundos is not None:
        _validar_timeout(data.timeout_segundos)

    if data.retries is not None:
        _validar_retries(data.retries)

    # Nombre único
    if data.nombre is not None and data.nombre.lower() != api.nombre.lower():
        existente = (
            db.query(Api)
            .filter(Api.nombre.ilike(data.nombre))
            .first()
        )
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe otra API con ese nombre")
        api.nombre = data.nombre.strip()

    # Actualizar campos
    for campo, valor in data.dict(exclude_unset=True).items():
        if campo in ["headers_por_defecto", "body_ejemplo", "auth_config"]:
            setattr(api, campo, json.dumps(valor) if valor else None)
        else:
            setattr(api, campo, valor)

    db.commit()
    db.refresh(api)
    return api


# ============================================================
#  ELIMINAR API
# ============================================================

def delete_api(db: Session, api_id: int) -> None:
    api = get_api(db, api_id)

    # Validar que no esté asociada a pasos
    usada = db.query(Paso).filter(Paso.api_id == api_id).first()
    if usada:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la API porque está asociada a pasos"
        )

    try:
        db.delete(api)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al eliminar la API")


# ============================================================
#  TEST API CALL
# ============================================================

def test_api_call(data: ApiTestRequest) -> ApiTestResponse:
    url = data.base_url.rstrip("/") + "/" + data.endpoint.lstrip("/")

    try:
        response = requests.request(
            method=data.metodo,
            url=url,
            headers=data.headers or {},
            json=data.body or None,
            timeout=data.timeout or 10
        )

        return ApiTestResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
            ok=response.ok,
            elapsed_ms=int(response.elapsed.total_seconds() * 1000)
        )

    except Exception as e:
        return ApiTestResponse(
            status_code=0,
            headers={},
            body=str(e),
            ok=False,
            elapsed_ms=0
        )
