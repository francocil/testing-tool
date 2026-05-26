"""
Tests para routes/paso_documento.py

Cubre:
- Listar documentos de paso
- Obtener documento por ID
- Crear documento (multipart/form-data)
- Actualizar documento (reemplazo de archivo)
- Eliminar documento

IMPORTANTE:
Tu router usa el prefix:
    /api/v1/pasos-documentos

Y los endpoints reales son:
    GET    /pasos-documentos/
    GET    /pasos-documentos/{id}
    POST   /pasos-documentos/          (multipart/form-data)
    PUT    /pasos-documentos/{id}      (multipart/form-data)
    DELETE /pasos-documentos/{id}

ACLARACIÓN SOBRE UPDATE:
Tu service update_paso_documento SOLO actualiza:
    - archivo_url (si se envía un archivo nuevo)
NO actualiza:
    - paso_id
    - fecha_subida
"""

import io
import pytest
from models.proyecto import Proyecto
from models.modulo import Modulo
from models.caso_prueba import CasoPrueba
from models.paso import Paso
from models.paso_documento import PasoDocumento


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


def crear_documento_en_db(db, paso_id, url="http://test.com/doc.pdf"):
    doc = PasoDocumento(
        paso_id=paso_id,
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
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)

    crear_documento_en_db(db, paso.id, "http://test.com/a.pdf")
    crear_documento_en_db(db, paso.id, "http://test.com/b.pdf")

    resp = client.get("/api/v1/pasos-documentos/")
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
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    doc = crear_documento_en_db(db, paso.id)

    resp = client.get(f"/api/v1/pasos-documentos/{doc.id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == doc.id
    assert data["archivo_url"] == doc.archivo_url


def test_obtener_documento_inexistente(client):
    resp = client.get("/api/v1/pasos-documentos/9999")
    assert resp.status_code == 404


def test_crear_documento(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)

    file_content = b"contenido de prueba"
    file = io.BytesIO(file_content)

    resp = client.post(
        "/api/v1/pasos-documentos/",
        files={"archivo": ("test.pdf", file, "application/pdf")},
        data={"paso_id": paso.id}
    )

    assert resp.status_code == 201

    data = resp.json()
    assert data["paso_id"] == paso.id
    assert "test.pdf" in data["archivo_url"]


def test_actualizar_documento(client, db):
    """
    ACLARACIÓN:
    update_paso_documento SOLO reemplaza el archivo.
    NO cambia:
        - paso_id
        - fecha_subida
    """
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    doc = crear_documento_en_db(db, paso.id, "http://old.com/old.pdf")

    new_file = io.BytesIO(b"nuevo contenido")

    resp = client.put(
        f"/api/v1/pasos-documentos/{doc.id}",
        files={"archivo": ("nuevo.pdf", new_file, "application/pdf")}
    )

    assert resp.status_code == 200

    data = resp.json()
    assert data["paso_id"] == paso.id
    assert "nuevo.pdf" in data["archivo_url"]


def test_actualizar_documento_inexistente(client, db):
    new_file = io.BytesIO(b"x")

    resp = client.put(
        "/api/v1/pasos-documentos/9999",
        files={"archivo": ("x.pdf", new_file, "application/pdf")}
    )

    assert resp.status_code == 404


def test_eliminar_documento(client, db):
    proyecto = crear_proyecto_en_db(db)
    modulo = crear_modulo_en_db(db, proyecto.id)
    caso = crear_caso_en_db(db, modulo.id)
    paso = crear_paso_en_db(db, caso.id)
    doc = crear_documento_en_db(db, paso.id)

    resp = client.delete(f"/api/v1/pasos-documentos/{doc.id}")
    assert resp.status_code == 204

    resp2 = client.get(f"/api/v1/pasos-documentos/{doc.id}")
    assert resp2.status_code == 404
