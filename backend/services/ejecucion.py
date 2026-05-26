from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.ejecucion import Ejecucion
from models.caso_prueba import CasoPrueba
from models.usuario import Usuario
from models.paso import Paso

from schemas.ejecucion import EjecucionCreate, EjecucionUpdate


# ============================================================
#  CONSTANTES
# ============================================================

MODOS_VALIDOS = {"automatico", "paso_a_paso", "mixto", "simulado"}
ESTADOS_VALIDOS = {"pendiente", "en_progreso", "finalizado", "cancelado", "error"}


# ============================================================
#  HELPERS
# ============================================================

def _get_caso_or_404(db: Session, caso_id: int) -> CasoPrueba:
    caso = db.query(CasoPrueba).filter(CasoPrueba.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso de prueba no encontrado")
    return caso


def _get_ejecucion_or_404(db: Session, ejecucion_id: int) -> Ejecucion:
    ejec = db.query(Ejecucion).filter(Ejecucion.id == ejecucion_id).first()
    if not ejec:
        raise HTTPException(status_code=404, detail="Ejecución no encontrada")
    return ejec


def _validar_usuario(db: Session, usuario_id: int):
    if not db.query(Usuario).filter(Usuario.id == usuario_id).first():
        raise HTTPException(status_code=400, detail="Usuario no existe")


def _validar_modo(modo: str):
    if modo not in MODOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Modo inválido: {modo}. Valores permitidos: {', '.join(MODOS_VALIDOS)}"
        )


def _validar_estado(estado: str | None):
    if estado is None:
        return
    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido: {estado}. Valores permitidos: {', '.join(ESTADOS_VALIDOS)}"
        )


def _validar_pasos_existentes(db: Session, caso_id: int):
    if db.query(Paso).filter(Paso.caso_id == caso_id).count() == 0:
        raise HTTPException(status_code=400, detail="El caso no tiene pasos definidos")


def _validar_no_ejecucion_activa(db: Session, caso_id: int):
    activa = (
        db.query(Ejecucion)
        .filter(
            Ejecucion.caso_id == caso_id,
            Ejecucion.estado.in_(["pendiente", "en_progreso"])
        )
        .first()
    )
    if activa:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una ejecución en progreso para este caso"
        )


# ============================================================
#  Crear Ejecución
# ============================================================

def create_ejecucion(db: Session, data: EjecucionCreate) -> Ejecucion:
    caso = _get_caso_or_404(db, data.caso_id)

    _validar_usuario(db, data.usuario_id)
    _validar_modo(data.modo)
    _validar_pasos_existentes(db, caso.id)
    _validar_no_ejecucion_activa(db, caso.id)

    if caso.estado != "activo":
        raise HTTPException(status_code=400, detail="El caso no está activo")

    ejec = Ejecucion(
        caso_id=caso.id,
        usuario_id=data.usuario_id,
        modo=data.modo,
        estado="pendiente",
        fecha=datetime.utcnow(),

        # Snapshot del caso
        caso_version=caso.version_actual,
        caso_nombre=caso.nombre,
        caso_objetivo=caso.objetivo,
        caso_precondiciones=caso.precondiciones,
        caso_postcondiciones=caso.postcondiciones,

        contexto={},
        resultado_global=None,
        porcentaje_aceptacion=None,
        duracion_ms=None,
    )

    db.add(ejec)
    db.commit()
    db.refresh(ejec)
    return ejec


# ============================================================
#  Obtener Ejecución
# ============================================================

def get_ejecucion(db: Session, ejecucion_id: int) -> Ejecucion:
    return _get_ejecucion_or_404(db, ejecucion_id)


# ============================================================
#  Listar Ejecuciones
# ============================================================

def list_ejecuciones(db: Session, caso_id: int | None = None):
    query = db.query(Ejecucion)
    if caso_id is not None:
        query = query.filter(Ejecucion.caso_id == caso_id)
    return query.order_by(Ejecucion.fecha.desc()).all()


# ============================================================
#  Actualizar Ejecución
# ============================================================

def update_ejecucion(db: Session, ejecucion_id: int, data: EjecucionUpdate) -> Ejecucion:
    ejec = _get_ejecucion_or_404(db, ejecucion_id)

    _validar_estado(data.estado)

    if data.contexto is not None and not isinstance(data.contexto, dict):
        raise HTTPException(status_code=400, detail="El contexto debe ser un objeto JSON")

    if data.porcentaje_aceptacion is not None:
        if data.porcentaje_aceptacion < 0 or data.porcentaje_aceptacion > 100:
            raise HTTPException(status_code=400, detail="El porcentaje debe estar entre 0 y 100")

    # No permitir modificar ejecuciones finalizadas
    if ejec.estado == "finalizado":
        raise HTTPException(status_code=400, detail="La ejecución ya está finalizada")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(ejec, campo, valor)

    # Calcular duración
    if data.fecha_fin:
        if data.fecha_fin < ejec.fecha:
            raise HTTPException(status_code=400, detail="La fecha de fin no puede ser anterior al inicio")

        ejec.duracion_ms = int((data.fecha_fin - ejec.fecha).total_seconds() * 1000)

    db.commit()
    db.refresh(ejec)
    return ejec


# ============================================================
#  Eliminar Ejecución
# ============================================================

def delete_ejecucion(db: Session, ejecucion_id: int):
    ejec = _get_ejecucion_or_404(db, ejecucion_id)

    try:
        db.delete(ejec)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la ejecución porque tiene pasos asociados"
        )

    return {"detail": "Ejecución eliminada correctamente"}
