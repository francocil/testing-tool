"""
Tests para routes/comentario.py

Cubre:
- Listar comentarios por entidad
- Obtener comentario por ID
- Crear comentario
- Actualizar comentario
- Eliminar comentario

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/comentarios

Y los endpoints reales son:
    GET    /comentarios/entidad/{entidad_tipo}/{entidad_id}
    GET    /comentarios/{id}
    POST   /comentarios/
    PUT    /comentarios/{id}
    DELETE /comentarios/{id}

ACLARACIÓN SOBRE UPDATE:
Tu service update_comentario normalmente actualiza:
    - comentario
    - entidad_tipo
    - entidad_id
    - ejecucion_id (si se envía)
NO actualiza:
    - usuario_id
    - fecha
"""

import pytest
from models.rol import Rol
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba
from models.ejecucion import Ejecucion
from models.comentario import Comentario, EntidadTipo


# ============================================================
# HELPERS
# ============================================================

def crear_rol_en_db(db):
    rol = Rol(nombre="Tester")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


def crear_usuario_en_db(db):
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


def crear_ejecucion_en_db(db, caso_id):
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


def crear_comentario_en_db(db, usuario_id, entidad_tipo, entidad_id, ejecucion_id=None):
    comentario = Comentario(
        usuario_id=usuario_id,
        entidad_tipo=entidad_tipo,
        entidad_id=entidad_id,
        ejecucion_id=ejecucion_id,
        comentario="Texto inicial"
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_comentarios_por_entidad(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    usuario = crear_usuario_en_db(db)

    c1 = crear_comentario_en_db(db, usuario.id, EntidadTipo.CASO, caso.id)
    c2 = crear_comentario_en_db(db, usuario.id, EntidadTipo.CASO, caso.id)

    resp = client.get(f"/api/v1/comentarios/entidad/caso/{caso.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 2
    assert {c["id"] for c in data} == {c1.id, c2.id}


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_comentario_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    usuario = crear_usuario_en_db(db)

    comentario = crear_comentario_en_db(db, usuario.id, EntidadTipo.CASO, caso.id)

    resp = client.get(f"/api/v1/comentarios/{comentario.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == comentario.id
    assert data["comentario"] == "Texto inicial"


def test_obtener_comentario_inexistente(client):
    resp = client.get("/api/v1/comentarios/9999")
    assert resp.status_code == 404


def test_crear_comentario(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    usuario = crear_usuario_en_db(db)

    payload = {
        "usuario_id": usuario.id,
        "entidad_tipo": "caso",
        "entidad_id": caso.id,
        "comentario": "Nuevo comentario",
        "ejecucion_id": None
    }

    resp = client.post("/api/v1/comentarios/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["usuario_id"] == usuario.id
    assert data["entidad_tipo"] == "caso"
    assert data["comentario"] == "Nuevo comentario"


def test_actualizar_comentario(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    usuario = crear_usuario_en_db(db)

    comentario = crear_comentario_en_db(db, usuario.id, EntidadTipo.CASO, caso.id)

    payload = {
        "comentario": "Actualizado",
        "entidad_tipo": "caso",
        "entidad_id": caso.id,
        "ejecucion_id": None
    }

    resp = client.put(f"/api/v1/comentarios/{comentario.id}", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["comentario"] == "Actualizado"
    assert data["entidad_tipo"] == "caso"


def test_actualizar_comentario_inexistente(client, db):
    payload = {
        "comentario": "Nada",
        "entidad_tipo": "caso",
        "entidad_id": 1
    }

    resp = client.put("/api/v1/comentarios/9999", json=payload)
    assert resp.status_code == 404


def test_eliminar_comentario(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    usuario = crear_usuario_en_db(db)

    comentario = crear_comentario_en_db(db, usuario.id, EntidadTipo.CASO, caso.id)

    resp = client.delete(f"/api/v1/comentarios/{comentario.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/comentarios/{comentario.id}")
    assert resp2.status_code == 404
