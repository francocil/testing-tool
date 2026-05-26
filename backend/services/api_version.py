from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
import json

from models.api_version import ApiVersion
from models.my_api import Api
from schemas.api_version import ApiVersionCreate


# ============================================================
#  Obtener todas las versiones de una API
# ============================================================
def get_versiones_de_api(db: Session, api_id: int) -> list[ApiVersion]:
    return (
        db.query(ApiVersion)
        .filter(ApiVersion.api_id == api_id)
        .order_by(ApiVersion.fecha_creacion.desc())
        .all()
    )


# ============================================================
#  Obtener una versión específica
# ============================================================
def get_version(db: Session, version_id: int) -> ApiVersion:
    version = (
        db.query(ApiVersion)
        .filter(ApiVersion.id == version_id)
        .first()
    )

    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Versión de API no encontrada"
        )

    return version


# ============================================================
#  Crear una nueva versión desde el estado actual de la API
# ============================================================
def crear_version_desde_api(
    db: Session,
    api_id: int,
    usuario_id: int | None = None
) -> ApiVersion:

    api = (
        db.query(Api)
        .filter(Api.id == api_id)
        .first()
    )

    if not api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API no encontrada"
        )

    nueva = ApiVersion(
        api_id=api.id,
        version=api.version,
        metodo=api.metodo,
        base_url=api.base_url,
        endpoint=api.endpoint,
        auth_tipo=api.auth_tipo,
        auth_config=api.auth_config,
        headers_por_defecto=api.headers_por_defecto,
        body_ejemplo=api.body_ejemplo,
        timeout_segundos=api.timeout_segundos,
        retries=api.retries,
        creado_por_usuario_id=usuario_id,
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# ============================================================
#  Crear versión manual (opcional)
# ============================================================
def crear_version_manual(db: Session, data: ApiVersionCreate) -> ApiVersion:
    nueva = ApiVersion(
        api_id=data.api_id,
        version=data.version,
        metodo=data.metodo,
        base_url=data.base_url,
        endpoint=data.endpoint,
        auth_tipo=data.auth_tipo,
        auth_config=json.dumps(data.auth_config) if data.auth_config else None,
        headers_por_defecto=json.dumps(data.headers_por_defecto) if data.headers_por_defecto else None,
        body_ejemplo=json.dumps(data.body_ejemplo) if data.body_ejemplo else None,
        timeout_segundos=data.timeout_segundos,
        retries=data.retries,
        creado_por_usuario_id=data.creado_por_usuario_id,
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# ============================================================
#  Rollback a una versión anterior
# ============================================================
def rollback_version(db: Session, version_id: int):
    version = db.query(ApiVersion).filter(ApiVersion.id == version_id).first()

    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")

    api = db.query(Api).filter(Api.id == version.api_id).first()

    if not api:
        raise HTTPException(status_code=404, detail="API original no encontrada")

    # Restaurar campos
    api.metodo = version.metodo
    api.base_url = version.base_url
    api.endpoint = version.endpoint
    api.auth_tipo = version.auth_tipo
    api.auth_config = version.auth_config
    api.headers_por_defecto = version.headers_por_defecto
    api.body_ejemplo = version.body_ejemplo
    api.timeout_segundos = version.timeout_segundos
    api.retries = version.retries
    api.version = version.version

    db.commit()
    db.refresh(api)

    # Crear versión automática post-rollback
    crear_version_desde_api(db, api.id, None)

    return {"ok": True, "msg": "API restaurada correctamente", "api_id": api.id}


# ============================================================
#  Clonar una versión
# ============================================================
def clonar_version(db: Session, version_id: int):
    version = (
        db.query(ApiVersion)
        .options(joinedload(ApiVersion.api))  # ← NECESARIO para acceder a version.api
        .filter(ApiVersion.id == version_id)
        .first()
    )

    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")

    # Crear nombre nuevo
    base_name = f"{version.api.nombre}_clone"
    contador = 1

    nuevo_nombre = f"{base_name}_{contador}"
    while db.query(Api).filter(Api.nombre == nuevo_nombre).first():
        contador += 1
        nuevo_nombre = f"{base_name}_{contador}"

    nueva_api = Api(
        nombre=nuevo_nombre,
        descripcion=version.api.descripcion,  # ← FIX: se toma de la API original
        metodo=version.metodo,
        base_url=version.base_url,
        endpoint=version.endpoint,
        auth_tipo=version.auth_tipo,
        auth_config=version.auth_config,
        headers_por_defecto=version.headers_por_defecto,
        body_ejemplo=version.body_ejemplo,
        timeout_segundos=version.timeout_segundos,
        retries=version.retries,
        version=version.version,
        activo=1
    )

    db.add(nueva_api)
    db.commit()
    db.refresh(nueva_api)

    # Crear versión inicial de la API clonada
    crear_version_desde_api(db, nueva_api.id, None)

    return {
        "ok": True,
        "msg": "API clonada correctamente",
        "api_id": nueva_api.id
    }
