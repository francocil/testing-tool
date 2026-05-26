"""
Tests para routes/ejecucion_paso.py

Cubre:
- Listar ejecuciones de paso por ejecución
- Obtener ejecución de paso por ID
- Crear ejecución de paso
- Actualizar ejecución de paso
- Eliminar ejecución de paso

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/ejecuciones-pasos

Y los endpoints reales son:
    GET    /ejecuciones-pasos/ejecucion/{ejecucion_id}
    GET    /ejecuciones-pasos/{id}
    POST   /ejecuciones-pasos/
    PUT    /ejecuciones-pasos/{id}
    DELETE /ejecuciones-pasos/{id}

ACLARACIÓN SOBRE UPDATE:
Tu service update_ejecucion_paso SOLO actualiza:
    - resultado
    - valor_obtenido
NO actualiza:
    - ejecucion_id
    - paso_id
    - fecha
"""

import pytest
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba
from models.paso import Paso
from models.ejecucion import Ejecucion
from models.ejecucion_paso import EjecucionPaso
from models.usuario import Usuario
from models.rol import Rol


# ============================================================
# HELPERS
# ============================================================

def crear_rol_en_db(db):
    """
    Crea un rol mínimo para permitir crear usuarios.
    """
    rol = Rol(nombre="Tester")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


def crear_usuario_en_db(db):
    """
    Crea un usuario válido según tu modelo real.
    Campos obligatorios:
        - nombre
        - email (único)
        - password_hash
        - rol_id
    """
    rol = crear_rol_en_db(db)

    usuario = Usuario(
        nombre="Usuario Test",
        email="usuario_test@example.com",
        password_hash="hash123",
        rol_id=rol.id,
        activo=True
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def crear_proyecto_en_db(db):
    proyecto = Proyecto(
        nombre="Proyecto Test",
        objetivo_general="Objetivo",
        contexto="Contexto"
    )
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def crear_modulo_en_db(db, proyecto_id):
    modulo = Modulo(
        proyecto_id=proyecto_id,
        nombre="Modulo Test",
        tipo_interfaz="API",
        tipo_gui="web",
        descripcion="desc"
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return modulo


def crear_caso_en_db(db, modulo_id):
    caso = CasoPrueba(
        nombre="Caso Test",
        objetivo="Objetivo",
        modulo_id=modulo_id,
        porcentaje_aceptacion=100.0
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


def crear_paso_en_db(db, caso_id):
    paso = Paso(
        caso_id=caso_id,
        orden=1,
        descripcion="Paso Test"
    )
    db.add(paso)
    db.commit()
    db.refresh(paso)
    return paso


def crear_ejecucion_en_db(db, caso_id):
    """
    Crea una ejecución válida según tu modelo real.
    Campos obligatorios:
        - caso_id
        - usuario_id
        - modo (default: mixto)
        - estado (default: pendiente)
    """
    usuario = crear_usuario_en_db(db)

    ejecucion = Ejecucion(
        caso_id=caso_id,
        usuario_id=usuario.id,
        modo="mixto",
        estado="pendiente",
        resultado_global=None,
        porcentaje_aceptacion=None
    )
    db.add(ejecucion)
    db.commit()
    db.refresh(ejecucion)
    return ejecucion


def crear_ejecucion_paso_en_db(db, ejecucion_id, paso_id, resultado="OK"):
    ejec_paso = EjecucionPaso(
        ejecucion_id=ejecucion_id,
        paso_id=paso_id,
        resultado=resultado,
        valor_obtenido="valor inicial"
    )
    db.add(ejec_paso)
    db.commit()
    db.refresh(ejec_paso)
    return ejec_paso


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_ejecuciones_paso_por_ejecucion(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    ejecucion = crear_ejecucion_en_db(db, caso.id)

    crear_ejecucion_paso_en_db(db, ejecucion.id, paso.id, resultado="OK")
    crear_ejecucion_paso_en_db(db, ejecucion.id, paso.id, resultado="ERROR")

    resp = client.get(f"/api/v1/ejecuciones-pasos/ejecucion/{ejecucion.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 2
    assert {e["resultado"] for e in data} == {"OK", "ERROR"}


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_ejecucion_paso_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    ejecucion = crear_ejecucion_en_db(db, caso.id)

    ejec_paso = crear_ejecucion_paso_en_db(db, ejecucion.id, paso.id)

    resp = client.get(f"/api/v1/ejecuciones-pasos/{ejec_paso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == ejec_paso.id
    assert data["resultado"] == "OK"


def test_obtener_ejecucion_paso_inexistente(client):
    resp = client.get("/api/v1/ejecuciones-pasos/9999")
    assert resp.status_code == 404


def test_crear_ejecucion_paso(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    ejecucion = crear_ejecucion_en_db(db, caso.id)

    payload = {
        "ejecucion_id": ejecucion.id,
        "paso_id": paso.id,
        "resultado": "OK",
        "valor_obtenido": "respuesta"
    }

    resp = client.post("/api/v1/ejecuciones-pasos/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["ejecucion_id"] == ejecucion.id
    assert data["paso_id"] == paso.id
    assert data["resultado"] == "OK"


def test_actualizar_ejecucion_paso(client, db):
    """
    ACLARACIÓN:
    Tu service update_ejecucion_paso SOLO actualiza:
        - resultado
        - valor_obtenido
    NO actualiza:
        - ejecucion_id
        - paso_id
        - fecha
    """
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    ejecucion = crear_ejecucion_en_db(db, caso.id)

    ejec_paso = crear_ejecucion_paso_en_db(db, ejecucion.id, paso.id)

    payload = {
        "ejecucion_id": ejecucion.id,   # NO se actualiza
        "paso_id": paso.id,             # NO se actualiza
        "resultado": "ERROR",           # SÍ se actualiza
        "valor_obtenido": "nuevo valor" # SÍ se actualiza
    }

    resp = client.put(f"/api/v1/ejecuciones-pasos/{ejec_paso.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()

    # Campos que NO cambian
    assert data["ejecucion_id"] == ejecucion.id
    assert data["paso_id"] == paso.id

    # Campos que SÍ cambian
    assert data["resultado"] == "ERROR"
    assert data["valor_obtenido"] == "nuevo valor"


def test_actualizar_ejecucion_paso_inexistente(client, db):
    payload = {
        "resultado": "OK",
        "valor_obtenido": "x"
    }

    resp = client.put("/api/v1/ejecuciones-pasos/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_ejecucion_paso(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    ejecucion = crear_ejecucion_en_db(db, caso.id)

    ejec_paso = crear_ejecucion_paso_en_db(db, ejecucion.id, paso.id)

    resp = client.delete(f"/api/v1/ejecuciones-pasos/{ejec_paso.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/ejecuciones-pasos/{ejec_paso.id}")
    assert resp2.status_code == 404
