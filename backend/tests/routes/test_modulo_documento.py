"""
Tests para routes/modulo_documento.py

Cubre:
- Listar documentos de módulo
- Obtener documento por ID
- Crear documento (multipart/form-data)
- Actualizar documento (reemplazo de archivo)
- Eliminar documento

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/modulo-documentos

Y los endpoints reales son:
    GET    /modulo-documentos/
    GET    /modulo-documentos/{id}
    POST   /modulo-documentos/          (multipart/form-data)
    PUT    /modulo-documentos/{id}      (multipart/form-data)
    DELETE /modulo-documentos/{id}

ACLARACIÓN SOBRE UPDATE:
Tu service update_modulo_documento SOLO actualiza:
    - archivo_url (si se envía un archivo nuevo)
NO actualiza:
    - modulo_id
    - fecha_subida
"""

import io
import pytest
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.modulo_documento import ModuloDocumento


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


def crear_documento_en_db(db, modulo_id, url="http://test.com/doc.pdf"):
    doc = ModuloDocumento(
        modulo_id=modulo_id,
        archivo_url=url
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
    modulo = crear_modulo_en_db(db, proyecto.id)

    crear_documento_en_db(db, modulo.id, "http://test.com/a.pdf")
    crear_documento_en_db(db, modulo.id, "http://test.com/b.pdf")

    resp = client.get("/api/v1/modulo-documentos/")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 2
    assert {"http://test.com/a.pdf", "http://test.com/b.pdf"}.issubset(
        {d["archivo_url"] for d in data}
    )


# ============================================================
# TESTS CRUD
# ============================================================

def test_obtener_documento_por_id(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    doc = crear_documento_en_db(db, modulo.id)

    resp = client.get(f"/api/v1/modulo-documentos/{doc.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == doc.id
    assert data["archivo_url"] == doc.archivo_url


def test_obtener_documento_inexistente(client):
    resp = client.get("/api/v1/modulo-documentos/9999")
    assert resp.status_code == 404


def test_crear_documento(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)

    # Simular archivo subido
    file_content = b"contenido de prueba"
    file = io.BytesIO(file_content)

    resp = client.post(
        "/api/v1/modulo-documentos/",
        files={"archivo": ("test.pdf", file, "application/pdf")},
        data={"modulo_id": modulo.id}
    )

    assert resp.status_code == 201

    data = resp.json()
    assert data["modulo_id"] == modulo.id
    assert "test.pdf" in data["archivo_url"]  # depende de tu service


def test_actualizar_documento(client, db):
    """
    ACLARACIÓN:
    update_modulo_documento SOLO reemplaza el archivo.
    NO cambia:
        - modulo_id
        - fecha_subida
    """
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    doc = crear_documento_en_db(db, modulo.id, "http://old.com/old.pdf")

    new_file = io.BytesIO(b"nuevo contenido")

    resp = client.put(
        f"/api/v1/modulo-documentos/{doc.id}",
        files={"archivo": ("nuevo.pdf", new_file, "application/pdf")}
    )

    assert resp.status_code == 200

    data = resp.json()
    assert data["modulo_id"] == modulo.id
    assert "nuevo.pdf" in data["archivo_url"]


def test_actualizar_documento_inexistente(client, db):
    new_file = io.BytesIO(b"x")

    resp = client.put(
        "/api/v1/modulo-documentos/9999",
        files={"archivo": ("x.pdf", new_file, "application/pdf")}
    )

    assert resp.status_code == 404


def test_eliminar_documento(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    doc = crear_documento_en_db(db, modulo.id)

    resp = client.delete(f"/api/v1/modulo-documentos/{doc.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/modulo-documentos/{doc.id}")
    assert resp2.status_code == 404
