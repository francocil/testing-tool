"""
Tests para routes/proyecto_documento.py

Cubre:
- Listar documentos de proyecto
- Obtener documento por ID
- Crear documento (multipart/form-data)
- Actualizar documento (archivo y/o descripción)
- Eliminar documento

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/proyecto-documentos

Y los endpoints reales son:
    GET    /proyecto-documentos/
    GET    /proyecto-documentos/{id}
    POST   /proyecto-documentos/          (multipart/form-data)
    PUT    /proyecto-documentos/{id}      (multipart/form-data)
    DELETE /proyecto-documentos/{id}

ACLARACIÓN SOBRE UPDATE:
Tu service update_proyecto_documento puede actualizar:
    - archivo_url (si se envía archivo nuevo)
    - descripcion (si se envía)
NO actualiza:
    - proyecto_id
    - fecha_subida
"""

import io
import pytest
from models.proyecto import Proyecto
from models.proyecto_documento import ProyectoDocumento


# ============================================================
# HELPERS
# ============================================================

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


def crear_documento_en_db(db, proyecto_id, url="http://test.com/doc.pdf", descripcion=None):
    doc = ProyectoDocumento(
        proyecto_id=proyecto_id,
        archivo_url=url,
        descripcion=descripcion
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


# ============================================================
# TESTS LISTADO
# ============================================================

def test_listar_documentos(client, db):
    proyecto = crear_proyecto_en_db(db)

    crear_documento_en_db(db, proyecto.id, "http://test.com/a.pdf", "Doc A")
    crear_documento_en_db(db, proyecto.id, "http://test.com/b.pdf", "Doc B")

    resp = client.get("/api/v1/proyecto-documentos/")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 2
    urls = {d["archivo_url"] for d in data}
    assert {"http://test.com/a.pdf", "http://test.com/b.pdf"}.issubset(urls)


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_documento_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, proyecto.id, "http://test.com/doc.pdf", "Inicial")

    resp = client.get(f"/api/v1/proyecto-documentos/{doc.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == doc.id
    assert data["archivo_url"] == doc.archivo_url
    assert data["descripcion"] == "Inicial"


def test_obtener_documento_inexistente(client):
    resp = client.get("/api/v1/proyecto-documentos/9999")
    assert resp.status_code == 404


def test_crear_documento(client, db):
    proyecto = crear_proyecto_en_db(db)

    file_content = b"contenido de prueba"
    file = io.BytesIO(file_content)

    resp = client.post(
        "/api/v1/proyecto-documentos/",
        files={"archivo": ("test.pdf", file, "application/pdf")},
        data={
            "proyecto_id": proyecto.id,
            "descripcion": "Documento creado"
        }
    )

    assert resp.status_code == 201

    data = resp.json()
    assert data["proyecto_id"] == proyecto.id
    assert data["descripcion"] == "Documento creado"
    assert "test.pdf" in data["archivo_url"]


def test_actualizar_documento_solo_descripcion(client, db):
    proyecto = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, proyecto.id, "http://test.com/doc.pdf", "Vieja desc")

    resp = client.put(
        f"/api/v1/proyecto-documentos/{doc.id}",
        data={"descripcion": "Nueva descripcion"}
    )

    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == doc.id
    assert data["proyecto_id"] == proyecto.id
    assert data["descripcion"] == "Nueva descripcion"
    assert data["archivo_url"] == "http://test.com/doc.pdf"


def test_actualizar_documento_archivo_y_descripcion(client, db):
    proyecto = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, proyecto.id, "http://old.com/old.pdf", "Vieja desc")

    new_file = io.BytesIO(b"nuevo contenido")

    resp = client.put(
        f"/api/v1/proyecto-documentos/{doc.id}",
        files={"archivo": ("nuevo.pdf", new_file, "application/pdf")},
        data={"descripcion": "Descripcion actualizada"}
    )

    assert resp.status_code == 200

    data = resp.json()
    assert data["proyecto_id"] == proyecto.id
    assert data["descripcion"] == "Descripcion actualizada"
    assert "nuevo.pdf" in data["archivo_url"]


def test_actualizar_documento_inexistente(client, db):
    new_file = io.BytesIO(b"x")

    resp = client.put(
        "/api/v1/proyecto-documentos/9999",
        files={"archivo": ("x.pdf", new_file, "application/pdf")},
        data={"descripcion": "x"}
    )

    assert resp.status_code == 404


def test_eliminar_documento(client, db):
    proyecto = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, proyecto.id)

    resp = client.delete(f"/api/v1/proyecto-documentos/{doc.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/proyecto-documentos/{doc.id}")
    assert resp2.status_code == 404
