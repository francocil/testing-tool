"""
Tests para services/proyecto_documento.py

Cubre:
- get_proyecto_documentos
- get_proyecto_documento
- create_proyecto_documento
- update_proyecto_documento
- delete_proyecto_documento

Incluye:
- Mock de save_file, replace_file, delete_file
- Manejo correcto de errores HTTP
"""

import io
import pytest
from fastapi import HTTPException, UploadFile

from services.proyecto_documento import (
    get_proyecto_documentos,
    get_proyecto_documento,
    create_proyecto_documento,
    update_proyecto_documento,
    delete_proyecto_documento,
)

from services.proyecto import create_proyecto
from schemas.proyecto import ProyectoCreate
from models.proyecto_documento import ProyectoDocumento


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto X"):
    return create_proyecto(
        db,
        ProyectoCreate(
            nombre=nombre,
            objetivo_general="Objetivo general",
            contexto="Contexto"
        )
    )


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
# MOCKS FILE SERVICE
# ============================================================

@pytest.fixture
def mock_save_file(monkeypatch):
    def fake_save(file, folder):
        return f"/fake/{folder}/{file.filename}"
    monkeypatch.setattr("services.proyecto_documento.save_file", fake_save)


@pytest.fixture
def mock_replace_file(monkeypatch):
    def fake_replace(old, file, folder):
        return f"/fake/{folder}/new_{file.filename}"
    monkeypatch.setattr("services.proyecto_documento.replace_file", fake_replace)


@pytest.fixture
def mock_delete_file(monkeypatch):
    monkeypatch.setattr("services.proyecto_documento.delete_file", lambda x: None)


# ============================================================
# TESTS GET
# ============================================================

def test_get_proyecto_documentos(db):
    p = crear_proyecto_en_db(db)

    crear_documento_en_db(db, p.id, "http://a.pdf")
    crear_documento_en_db(db, p.id, "http://b.pdf")

    docs = get_proyecto_documentos(db)
    assert len(docs) == 2
    assert {d.archivo_url for d in docs} == {"http://a.pdf", "http://b.pdf"}


def test_get_proyecto_documento_existente(db):
    p = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, p.id)

    resultado = get_proyecto_documento(db, doc.id)
    assert resultado.id == doc.id
    assert resultado.archivo_url == doc.archivo_url


def test_get_proyecto_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_proyecto_documento(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Documento de proyecto no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_proyecto_documento(db, mock_save_file):
    p = crear_proyecto_en_db(db)

    file = UploadFile(filename="test.pdf", file=io.BytesIO(b"contenido"))

    doc = create_proyecto_documento(db, p.id, file, descripcion="Manual")

    assert doc.id is not None
    assert doc.proyecto_id == p.id
    assert doc.archivo_url == "/fake/documentos_proyecto/test.pdf"
    assert doc.descripcion == "Manual"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_proyecto_documento(db, mock_replace_file):
    p = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, p.id, "http://old.pdf", "Viejo")

    new_file = UploadFile(filename="nuevo.pdf", file=io.BytesIO(b"nuevo"))

    actualizado = update_proyecto_documento(db, doc.id, new_file, "Nuevo desc")

    assert actualizado.archivo_url == "/fake/documentos_proyecto/new_nuevo.pdf"
    assert actualizado.descripcion == "Nuevo desc"


def test_update_proyecto_documento_solo_descripcion(db):
    p = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, p.id, "http://old.pdf", "Viejo")

    actualizado = update_proyecto_documento(db, doc.id, descripcion="Solo desc")

    assert actualizado.archivo_url == "http://old.pdf"
    assert actualizado.descripcion == "Solo desc"


def test_update_proyecto_documento_inexistente(db):
    new_file = UploadFile(filename="x.pdf", file=io.BytesIO(b"x"))

    with pytest.raises(HTTPException) as exc:
        update_proyecto_documento(db, 9999, new_file)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_proyecto_documento(db, mock_delete_file):
    p = crear_proyecto_en_db(db)
    doc = crear_documento_en_db(db, p.id)

    delete_proyecto_documento(db, doc.id)

    with pytest.raises(HTTPException):
        get_proyecto_documento(db, doc.id)


def test_delete_proyecto_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_proyecto_documento(db, 9999)

    assert exc.value.status_code == 404
