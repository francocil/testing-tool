from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.caso_prueba import CasoPrueba
from models.caso_prueba_version import CasoPruebaVersion
from models.modulo import Modulo
from models.paso import Paso

from schemas.caso_prueba import CasoPruebaCreate, CasoPruebaUpdate


# ============================================================
#  ESTADOS PERMITIDOS
# ============================================================

ESTADOS_VALIDOS = {"activo", "inactivo", "borrador", "archivado"}


def _validar_estado(estado: str | None):
    if estado is None:
        return
    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido: {estado}. Valores permitidos: {', '.join(ESTADOS_VALIDOS)}"
        )


# ============================================================
#  VALIDACIONES
# ============================================================

def _validar_modulo(db: Session, modulo_id: int):
    if not db.query(Modulo).filter(Modulo.id == modulo_id).first():
        raise HTTPException(status_code=400, detail="El módulo indicado no existe")


def _validar_porcentaje(valor: float | None):
    if valor is None:
        return
    if valor < 0 or valor > 100:
        raise HTTPException(status_code=400, detail="El porcentaje de aceptación debe estar entre 0 y 100")


def _validar_pasos_existentes(db: Session, caso_id: int):
    pasos = db.query(Paso).filter(Paso.caso_id == caso_id).count()
    if pasos == 0:
        raise HTTPException(status_code=400, detail="El caso no puede estar activo sin pasos")


# ============================================================
#  Crear Caso de Prueba
# ============================================================

def create_caso_prueba(db: Session, data: CasoPruebaCreate) -> CasoPrueba:

    _validar_estado(data.estado)
    _validar_modulo(db, data.modulo_id)
    _validar_porcentaje(data.porcentaje_aceptacion)

    # Validar nombre único dentro del módulo (case-insensitive)
    existente = (
        db.query(CasoPrueba)
        .filter(
            CasoPrueba.modulo_id == data.modulo_id,
            CasoPrueba.nombre.ilike(data.nombre)
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un caso de prueba con ese nombre en este módulo."
        )

    nuevo = CasoPrueba(
        modulo_id=data.modulo_id,
        nombre=data.nombre.strip(),
        objetivo=data.objetivo,
        descripcion=data.descripcion,
        precondiciones=data.precondiciones,
        postcondiciones=data.postcondiciones,
        estado=data.estado or "borrador",
        porcentaje_aceptacion=data.porcentaje_aceptacion,
        version_actual=1,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Crear versión inicial
    version = CasoPruebaVersion(
        caso_id=nuevo.id,
        nro_version=1,
        objetivo=nuevo.objetivo,
        porcentaje_aceptacion=nuevo.porcentaje_aceptacion,
        fecha=nuevo.fecha_creacion
    )
    db.add(version)
    db.commit()

    return nuevo


# ============================================================
#  Obtener Caso por ID
# ============================================================

def get_caso_prueba(db: Session, caso_id: int) -> CasoPrueba:
    caso = db.query(CasoPrueba).filter(CasoPrueba.id == caso_id).first()
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso de prueba no encontrado"
        )
    return caso


# ============================================================
#  Listar Casos por módulo
# ============================================================

def get_casos_por_modulo(db: Session, modulo_id: int):
    return (
        db.query(CasoPrueba)
        .filter(CasoPrueba.modulo_id == modulo_id)
        .order_by(CasoPrueba.nombre.asc())
        .all()
    )


# ============================================================
#  Actualizar Caso de Prueba
# ============================================================

def update_caso_prueba(db: Session, caso_id: int, data: CasoPruebaUpdate) -> CasoPrueba:
    caso = get_caso_prueba(db, caso_id)

    _validar_estado(data.estado)
    _validar_porcentaje(data.porcentaje_aceptacion)

    # Si pasa a activo, debe tener pasos
    if data.estado == "activo":
        _validar_pasos_existentes(db, caso_id)

    # Validar nombre único si cambia
    if data.nombre and data.nombre.lower() != caso.nombre.lower():
        existente = (
            db.query(CasoPrueba)
            .filter(
                CasoPrueba.modulo_id == caso.modulo_id,
                CasoPrueba.nombre.ilike(data.nombre),
                CasoPrueba.id != caso.id,
            )
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un caso de prueba con ese nombre en este módulo."
            )

    # Actualizar campos
    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(caso, campo, valor)

    # Versionado automático
    caso.version_actual += 1

    db.commit()
    db.refresh(caso)

    # Crear nueva versión
    version = CasoPruebaVersion(
        caso_id=caso.id,
        nro_version=caso.version_actual,
        objetivo=caso.objetivo,
        porcentaje_aceptacion=caso.porcentaje_aceptacion,
        fecha=caso.fecha_creacion
    )
    db.add(version)
    db.commit()

    return caso


# ============================================================
#  Eliminar Caso de Prueba
# ============================================================

def delete_caso_prueba(db: Session, caso_id: int):
    caso = get_caso_prueba(db, caso_id)

    try:
        db.delete(caso)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el caso porque tiene elementos asociados"
        )

    return True
