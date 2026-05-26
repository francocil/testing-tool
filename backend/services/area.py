from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.area import Area
from models.direccion import Direccion
from schemas.area import AreaCreate, AreaUpdate


# -----------------------------
# Obtener todas las áreas
# -----------------------------
def get_areas(db: Session) -> list[Area]:
    return db.query(Area).all()


# -----------------------------
# Obtener área por ID
# -----------------------------
def get_area(db: Session, area_id: int) -> Area:
    area = (
        db.query(Area)
        .filter(Area.id == area_id)
        .first()
    )

    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Área no encontrada"
        )

    return area


# -----------------------------
# Crear área
# -----------------------------
def create_area(db: Session, data: AreaCreate) -> Area:
    # Validar que exista la dirección
    direccion = (
        db.query(Direccion)
        .filter(Direccion.id == data.direccion_id)
        .first()
    )

    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )

    nueva = Area(
        direccion_id=data.direccion_id,
        nombre=data.nombre,
        descripcion=data.descripcion,
        activo=data.activo,
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# -----------------------------
# Actualizar área
# -----------------------------
def update_area(db: Session, area_id: int, data: AreaUpdate) -> Area:
    area = get_area(db, area_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(area, field, value)

    db.commit()
    db.refresh(area)

    return area


# -----------------------------
# Eliminar área
# -----------------------------
def delete_area(db: Session, area_id: int) -> None:
    area = get_area(db, area_id)

    db.delete(area)
    db.commit()
