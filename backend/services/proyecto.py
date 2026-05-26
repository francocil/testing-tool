from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.proyecto import Proyecto
from models.reparticion import Reparticion
from models.direccion import Direccion
from models.area import Area

from schemas.proyecto import ProyectoCreate, ProyectoUpdate


# ============================================================
#  ESTADOS PERMITIDOS
# ============================================================

ESTADOS_VALIDOS = {"activo", "inactivo", "archivado", "borrador"}


def _validar_estado(estado: str | None):
    if estado is None:
        return
    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido: {estado}. Valores permitidos: {', '.join(ESTADOS_VALIDOS)}"
        )


# ============================================================
#  VALIDACIONES INSTITUCIONALES
# ============================================================

def _validar_institucional(db: Session, reparticion_id: int | None, direccion_id: int | None, area_id: int | None):
    """
    Valida coherencia institucional:
    - Dirección debe pertenecer a Repartición
    - Área debe pertenecer a Dirección
    """

    # Validar Repartición
    if reparticion_id is not None:
        reparticion = db.query(Reparticion).filter(Reparticion.id == reparticion_id).first()
        if not reparticion:
            raise HTTPException(status_code=400, detail="Repartición no existe")

    # Validar Dirección
    if direccion_id is not None:
        direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
        if not direccion:
            raise HTTPException(status_code=400, detail="Dirección no existe")

        # Si hay repartición, validar coherencia
        if reparticion_id is not None and direccion.reparticion_id != reparticion_id:
            raise HTTPException(status_code=400, detail="La Dirección no pertenece a la Repartición indicada")

    # Validar Área
    if area_id is not None:
        area = db.query(Area).filter(Area.id == area_id).first()
        if not area:
            raise HTTPException(status_code=400, detail="Área no existe")

        # Si hay dirección, validar coherencia
        if direccion_id is not None and area.direccion_id != direccion_id:
            raise HTTPException(status_code=400, detail="El Área no pertenece a la Dirección indicada")


# ============================================================
#  Crear Proyecto
# ============================================================

def create_proyecto(db: Session, data: ProyectoCreate) -> Proyecto:

    _validar_estado(data.estado)
    _validar_institucional(db, data.reparticion_id, data.direccion_id, data.area_id)

    # Validar unicidad del nombre
    if db.query(Proyecto).filter(Proyecto.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un proyecto con ese nombre")

    proyecto = Proyecto(
        nombre=data.nombre,
        objetivo_general=data.objetivo_general,
        contexto=data.contexto,

        estado=data.estado,
        version=1,

        reparticion_id=data.reparticion_id,
        direccion_id=data.direccion_id,
        area_id=data.area_id,
    )

    db.add(proyecto)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al crear el proyecto")

    db.refresh(proyecto)
    return proyecto


# ============================================================
#  Obtener Proyecto por ID
# ============================================================

def get_proyecto(db: Session, proyecto_id: int) -> Proyecto:
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return proyecto


# ============================================================
#  Listar Proyectos
# ============================================================

def list_proyectos(db: Session) -> list[Proyecto]:
    return db.query(Proyecto).order_by(Proyecto.fecha_creacion.desc()).all()


# ============================================================
#  Actualizar Proyecto
# ============================================================

def update_proyecto(db: Session, proyecto_id: int, data: ProyectoUpdate) -> Proyecto:
    proyecto = get_proyecto(db, proyecto_id)

    _validar_estado(data.estado)
    _validar_institucional(db, data.reparticion_id, data.direccion_id, data.area_id)

    # Validar unicidad del nombre
    if data.nombre and data.nombre != proyecto.nombre:
        if db.query(Proyecto).filter(Proyecto.nombre == data.nombre).first():
            raise HTTPException(status_code=400, detail="Ya existe un proyecto con ese nombre")

    # Campos simples
    if data.nombre is not None:
        proyecto.nombre = data.nombre

    if data.objetivo_general is not None:
        proyecto.objetivo_general = data.objetivo_general

    if data.contexto is not None:
        proyecto.contexto = data.contexto

    if data.estado is not None:
        proyecto.estado = data.estado

    # Institucional
    if data.reparticion_id is not None:
        proyecto.reparticion_id = data.reparticion_id

    if data.direccion_id is not None:
        proyecto.direccion_id = data.direccion_id

    if data.area_id is not None:
        proyecto.area_id = data.area_id

    # Versionado automático
    proyecto.version += 1
    proyecto.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(proyecto)
    return proyecto


# ============================================================
#  Eliminar Proyecto
# ============================================================

def delete_proyecto(db: Session, proyecto_id: int) -> None:
    proyecto = get_proyecto(db, proyecto_id)

    try:
        db.delete(proyecto)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el proyecto porque tiene elementos asociados"
        )
