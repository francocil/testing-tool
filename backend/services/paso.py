from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.paso import Paso
from models.caso_prueba import CasoPrueba
from models.my_api import Api

from schemas.paso import PasoCreate, PasoUpdate


# ============================================================
#  TIPOS PERMITIDOS
# ============================================================

TIPOS_VALIDOS = {"manual", "automatico", "mixto", "simulado"}


def _validar_tipo(tipo: str | None):
    if tipo is None:
        return
    if tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de paso inválido: {tipo}. Valores permitidos: {', '.join(TIPOS_VALIDOS)}"
        )


# ============================================================
#  VALIDACIONES
# ============================================================

def _validar_caso(db: Session, caso_id: int):
    if not db.query(CasoPrueba).filter(CasoPrueba.id == caso_id).first():
        raise HTTPException(status_code=400, detail="El caso indicado no existe")


def _validar_api(db: Session, api_id: int | None):
    if api_id is None:
        return
    if not db.query(Api).filter(Api.id == api_id).first():
        raise HTTPException(status_code=400, detail="La API indicada no existe")


def _validar_orden(orden: int):
    if orden is None or orden < 1:
        raise HTTPException(status_code=400, detail="El orden debe ser un entero >= 1")


def _validar_json(valor, nombre: str):
    if valor is None:
        return
    if not isinstance(valor, dict):
        raise HTTPException(status_code=400, detail=f"{nombre} debe ser un objeto JSON válido")


def _validar_coherencia_tipo_api(tipo: str, api_id: int | None):
    if tipo in {"automatico", "mixto"} and api_id is None:
        raise HTTPException(status_code=400, detail="Los pasos automáticos o mixtos requieren una API asociada")

    if tipo == "manual" and api_id is not None:
        raise HTTPException(status_code=400, detail="Los pasos manuales no deben tener API asociada")


# ============================================================
#  Obtener Paso por ID
# ============================================================

def get_paso(db: Session, paso_id: int) -> Paso:
    paso = db.query(Paso).filter(Paso.id == paso_id).first()
    if not paso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paso no encontrado"
        )
    return paso


# ============================================================
#  Listar pasos de un caso (ordenados)
# ============================================================

def get_pasos_por_caso(db: Session, caso_id: int):
    return (
        db.query(Paso)
        .filter(Paso.caso_id == caso_id)
        .order_by(Paso.orden.asc())
        .all()
    )


# ============================================================
#  Crear Paso
# ============================================================

def create_paso(db: Session, data: PasoCreate) -> Paso:

    _validar_caso(db, data.caso_id)
    _validar_tipo(data.tipo)
    _validar_api(db, data.api_id)
    _validar_orden(data.orden)
    _validar_json(data.parametros_json, "parametros_json")
    _validar_json(data.extraccion_contexto, "extraccion_contexto")
    _validar_coherencia_tipo_api(data.tipo, data.api_id)

    # Validar orden único dentro del caso
    existente = (
        db.query(Paso)
        .filter(
            Paso.caso_id == data.caso_id,
            Paso.orden == data.orden
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un paso con orden {data.orden} en este caso."
        )

    paso = Paso(
        caso_id=data.caso_id,
        nombre=data.nombre.strip(),
        tipo=data.tipo,
        descripcion=data.descripcion,
        orden=data.orden,
        api_id=data.api_id,
        parametros_json=data.parametros_json,
        extraccion_contexto=data.extraccion_contexto,
    )

    db.add(paso)
    db.commit()
    db.refresh(paso)
    return paso


# ============================================================
#  Actualizar Paso
# ============================================================

def update_paso(db: Session, paso_id: int, data: PasoUpdate) -> Paso:
    paso = get_paso(db, paso_id)

    # Validaciones
    if data.tipo is not None:
        _validar_tipo(data.tipo)

    if data.api_id is not None:
        _validar_api(db, data.api_id)

    if data.orden is not None:
        _validar_orden(data.orden)

    if data.parametros_json is not None:
        _validar_json(data.parametros_json, "parametros_json")

    if data.extraccion_contexto is not None:
        _validar_json(data.extraccion_contexto, "extraccion_contexto")

    # Validar coherencia tipo/API
    tipo_final = data.tipo if data.tipo is not None else paso.tipo
    api_final = data.api_id if data.api_id is not None else paso.api_id
    _validar_coherencia_tipo_api(tipo_final, api_final)

    # Validar orden si cambia
    if data.orden is not None and data.orden != paso.orden:
        existente = (
            db.query(Paso)
            .filter(
                Paso.caso_id == paso.caso_id,
                Paso.orden == data.orden,
                Paso.id != paso.id
            )
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un paso con orden {data.orden} en este caso."
            )

    # Actualizar campos
    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(paso, campo, valor)

    db.commit()
    db.refresh(paso)
    return paso


# ============================================================
#  Eliminar Paso
# ============================================================

def delete_paso(db: Session, paso_id: int):
    paso = get_paso(db, paso_id)

    try:
        db.delete(paso)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el paso porque tiene elementos asociados"
        )

    return True
