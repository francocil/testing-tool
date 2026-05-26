from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from db.session import get_db

from services.proyecto import (
    get_proyecto,
    create_proyecto,
    update_proyecto,
    delete_proyecto,
)

from schemas.proyecto import ProyectoResponse, ProyectoCreate, ProyectoUpdate
from core.permissions import require_permission
from models.proyecto import Proyecto

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

# ===================================================
#  LISTAR PROYECTOS (FILTROS + PAGINACIÓN + ORDENAMIENTO)
# ===================================================
@router.get(
    "/",
    response_model=list[ProyectoResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("proyecto_ver_todos"))]
)
def listar_proyectos(
    nombre: str | None = None,
    estado: list[str] | None = None,

    reparticion_id: int | None = None,
    direccion_id: int | None = None,
    area_id: int | None = None,

    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,

    limit: int = 20,
    offset: int = 0,

    sort: str | None = None,

    db: Session = Depends(get_db)
):
    query = db.query(Proyecto)

    if nombre:
        query = query.filter(Proyecto.nombre.ilike(f"%{nombre}%"))

    if estado:
        query = query.filter(Proyecto.estado.in_(estado))

    if reparticion_id is not None:
        query = query.filter(Proyecto.reparticion_id == reparticion_id)

    if direccion_id is not None:
        query = query.filter(Proyecto.direccion_id == direccion_id)

    if area_id is not None:
        query = query.filter(Proyecto.area_id == area_id)

    if fecha_desde:
        query = query.filter(Proyecto.fecha_creacion >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Proyecto.fecha_creacion <= fecha_hasta)

    if sort:
        try:
            campo, orden = sort.split(":")
            orden = orden.lower()

            campos_validos = {
                "id": Proyecto.id,
                "nombre": Proyecto.nombre,
                "fecha_creacion": Proyecto.fecha_creacion,
                "fecha_actualizacion": Proyecto.fecha_actualizacion,
                "version": Proyecto.version,
            }

            if campo not in campos_validos:
                raise ValueError("Campo de ordenamiento inválido")

            columna = campos_validos[campo]

            if orden == "asc":
                query = query.order_by(asc(columna))
            elif orden == "desc":
                query = query.order_by(desc(columna))
            else:
                raise ValueError("Orden inválido (usar asc o desc)")

        except Exception:
            raise ValueError("Formato de sort inválido. Ej: sort=fecha_creacion:desc")
    else:
        query = query.order_by(Proyecto.fecha_creacion.desc())

    query = query.offset(offset).limit(limit)

    return query.all()


# ==========================
#  OBTENER PROYECTO POR ID
# ==========================
@router.get(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("proyecto_ver_proyecto"))]
)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return get_proyecto(db, proyecto_id)


# ==========================
#  CREAR PROYECTO
# ==========================
@router.post(
    "/",
    response_model=ProyectoResponse,
    status_code=201,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("proyecto_crear"))]
)
def crear_proyecto(data: ProyectoCreate, db: Session = Depends(get_db)):
    return create_proyecto(db, data)


# ==========================
#  ACTUALIZAR PROYECTO
# ==========================
@router.put(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(require_permission("proyecto_editar"))]
)
def actualizar_proyecto(proyecto_id: int, data: ProyectoUpdate, db: Session = Depends(get_db)):
    return update_proyecto(db, proyecto_id, data)


# ==========================
#  ELIMINAR PROYECTO
# ==========================
@router.delete(
    "/{proyecto_id}",
    status_code=204,
    dependencies=[Depends(require_permission("proyecto_eliminar"))]
)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    delete_proyecto(db, proyecto_id)
    return Response(status_code=204)
