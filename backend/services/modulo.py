from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException, status

from models.modulo import Modulo
from schemas.modulo import ModuloCreate, ModuloUpdate


# ============================================================
#  Crear Módulo
# ============================================================

def create_modulo(db: Session, data: ModuloCreate) -> Modulo:
    modulo = Modulo(
        nombre=data.nombre,
        tipo_interfaz=data.tipo_interfaz,
        tipo_gui=data.tipo_gui,
        descripcion=data.descripcion,

        estado=data.estado,
        version=data.version,
        responsable_id=data.responsable_id,

        proyecto_id=data.proyecto_id,
    )

    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return modulo


# ============================================================
#  Obtener Módulo por ID
# ============================================================

def get_modulo(db: Session, modulo_id: int) -> Modulo:
    modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if not modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
    return modulo


# ============================================================
#  Listar Módulos (con filtros, paginación y ordenamiento)
# ============================================================

def list_modulos(
    db: Session,
    proyecto_id: int | None = None,
    nombre: str | None = None,
    tipo_interfaz: str | None = None,
    tipo_gui: str | None = None,
    estado: list[str] | None = None,
    limit: int = 20,
    offset: int = 0,
    sort: str | None = None
) -> list[Modulo]:

    query = db.query(Modulo)

    # -----------------------------
    # Filtro por proyecto
    # -----------------------------
    if proyecto_id is not None:
        query = query.filter(Modulo.proyecto_id == proyecto_id)

    # -----------------------------
    # Filtro por nombre
    # -----------------------------
    if nombre:
        query = query.filter(Modulo.nombre.ilike(f"%{nombre}%"))

    # -----------------------------
    # Filtro por tipo de interfaz
    # -----------------------------
    if tipo_interfaz:
        query = query.filter(Modulo.tipo_interfaz == tipo_interfaz)

    # -----------------------------
    # Filtro por tipo de GUI
    # -----------------------------
    if tipo_gui:
        query = query.filter(Modulo.tipo_gui == tipo_gui)

    # -----------------------------
    # Filtro por estado (múltiple)
    # -----------------------------
    if estado:
        query = query.filter(Modulo.estado.in_(estado))

    # -----------------------------
    # Ordenamiento dinámico
    # -----------------------------
    if sort:
        try:
            campo, orden = sort.split(":")
            orden = orden.lower()

            campos_validos = {
                "id": Modulo.id,
                "nombre": Modulo.nombre,
                "fecha_creacion": Modulo.fecha_creacion,
                "fecha_actualizacion": Modulo.fecha_actualizacion,
                "version": Modulo.version,
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
        query = query.order_by(Modulo.fecha_creacion.desc())

    # -----------------------------
    # Paginación real
    # -----------------------------
    query = query.offset(offset).limit(limit)

    return query.all()


# ============================================================
#  Actualizar Módulo
# ============================================================

def update_modulo(db: Session, modulo_id: int, data: ModuloUpdate) -> Modulo:
    modulo = get_modulo(db, modulo_id)

    if data.nombre is not None:
        modulo.nombre = data.nombre

    if data.tipo_interfaz is not None:
        modulo.tipo_interfaz = data.tipo_interfaz

    if data.tipo_gui is not None:
        modulo.tipo_gui = data.tipo_gui

    if data.descripcion is not None:
        modulo.descripcion = data.descripcion

    if data.estado is not None:
        modulo.estado = data.estado

    if data.version is not None:
        modulo.version = data.version

    if data.responsable_id is not None:
        modulo.responsable_id = data.responsable_id

    db.commit()
    db.refresh(modulo)
    return modulo


# ============================================================
#  Eliminar Módulo
# ============================================================

def delete_modulo(db: Session, modulo_id: int) -> None:
    modulo = get_modulo(db, modulo_id)
    db.delete(modulo)
    db.commit()
