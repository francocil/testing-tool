from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.caso_prueba import (
    CasoPruebaCreate,
    CasoPruebaUpdate,
    CasoPrueba,
    CasoPruebaWithPasos,
)
from services.caso_prueba import (
    get_caso_prueba,
    get_casos_por_modulo,
    create_caso_prueba,
    update_caso_prueba,
    delete_caso_prueba,
)

from core.permissions import require_permission

router = APIRouter(prefix="/casos-prueba", tags=["Casos de Prueba"])


# ============================================================
# LISTAR POR MÓDULO
# ============================================================
@router.get(
    "/modulo/{modulo_id}",
    response_model=list[CasoPrueba],
    dependencies=[Depends(require_permission("caso_ver_modulo"))]
)
def listar_casos_por_modulo(modulo_id: int, db: Session = Depends(get_db)):
    return get_casos_por_modulo(db, modulo_id)


# ============================================================
# OBTENER POR ID
# ============================================================
@router.get(
    "/{caso_id}",
    response_model=CasoPruebaWithPasos,
    dependencies=[Depends(require_permission("caso_ver_modulo"))]
)
def obtener_caso(caso_id: int, db: Session = Depends(get_db)):
    return get_caso_prueba(db, caso_id)


# ============================================================
# CREAR
# ============================================================
@router.post(
    "/",
    response_model=CasoPrueba,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("caso_crear"))]
)
def crear_caso(data: CasoPruebaCreate, db: Session = Depends(get_db)):
    return create_caso_prueba(db, data)


# ============================================================
# ACTUALIZAR
# ============================================================
@router.put(
    "/{caso_id}",
    response_model=CasoPrueba,
    dependencies=[Depends(require_permission("caso_editar"))]
)
def actualizar_caso(caso_id: int, data: CasoPruebaUpdate, db: Session = Depends(get_db)):
    return update_caso_prueba(db, caso_id, data)


# ============================================================
# ELIMINAR
# ============================================================
@router.delete(
    "/{caso_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("caso_eliminar"))]
)
def eliminar_caso(caso_id: int, db: Session = Depends(get_db)):
    delete_caso_prueba(db, caso_id)
    return None
