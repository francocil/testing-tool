from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db.session import get_db
from services.objeto_parametro import (
    get_objeto_parametro,
    get_objetos_parametro_por_paso,
    get_objetos_parametro_por_api,
    create_objeto_parametro,
    update_objeto_parametro,
    delete_objeto_parametro,
)
from schemas.objeto_parametro import (
    ObjetoParametroCreate,
    ObjetoParametroUpdate,
    ObjetoParametroResponse,
)

# 🔐 Nuevo sistema de permisos
from core.permissions import require_permission


router = APIRouter(prefix="/objetos-parametros", tags=["ObjetoParametro"])


# -----------------------------
# Listar objetos parámetro por paso
# -----------------------------
@router.get(
    "/by-paso/{paso_id}",
    response_model=list[ObjetoParametroResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_parametros"))]
)
def listar_objetos_parametro_por_paso(paso_id: int, db: Session = Depends(get_db)):
    return get_objetos_parametro_por_paso(db, paso_id)


# -----------------------------
# Listar objetos parámetro por API
# -----------------------------
@router.get(
    "/by-api/{api_id}",
    response_model=list[ObjetoParametroResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_parametros"))]
)
def listar_objetos_parametro_por_api(api_id: int, db: Session = Depends(get_db)):
    return get_objetos_parametro_por_api(db, api_id)


# -----------------------------
# Obtener objeto parámetro por ID
# -----------------------------
@router.get(
    "/{objeto_parametro_id}",
    response_model=ObjetoParametroResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("ver_parametros"))]
)
def obtener_objeto_parametro(objeto_parametro_id: int, db: Session = Depends(get_db)):
    return get_objeto_parametro(db, objeto_parametro_id)


# -----------------------------
# Crear objeto parámetro
# -----------------------------
@router.post(
    "/",
    response_model=ObjetoParametroResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("crear_parametros"))]
)
def crear_objeto_parametro_endpoint(data: ObjetoParametroCreate, db: Session = Depends(get_db)):
    return create_objeto_parametro(db, data)


# -----------------------------
# Actualizar objeto parámetro
# -----------------------------
@router.put(
    "/{objeto_parametro_id}",
    response_model=ObjetoParametroResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("editar_parametros"))]
)
def actualizar_objeto_parametro_endpoint(objeto_parametro_id: int, data: ObjetoParametroUpdate, db: Session = Depends(get_db)):
    return update_objeto_parametro(db, objeto_parametro_id, data)


# -----------------------------
# Eliminar objeto parámetro
# -----------------------------
@router.delete(
    "/{objeto_parametro_id}",
    status_code=204,
    dependencies=[Depends(require_permission("eliminar_parametros"))]
)
def eliminar_objeto_parametro_endpoint(objeto_parametro_id: int, db: Session = Depends(get_db)):
    delete_objeto_parametro(db, objeto_parametro_id)
    return Response(status_code=204)


# -----------------------------
# Actualizar SOLO valor_entrada
# -----------------------------
@router.put(
    "/{objeto_parametro_id}/valor",
    response_model=ObjetoParametroResponse,
    dependencies=[Depends(require_permission("editar_parametros"))]
)
def actualizar_valor_entrada(objeto_parametro_id: int, data: dict, db: Session = Depends(get_db)):
    """
    Actualiza solo valor_entrada de un parámetro.
    """
    nuevo_valor = data.get("valor_entrada")
    return update_objeto_parametro(db, objeto_parametro_id, {"valor_entrada": nuevo_valor})
