"""
Tests para services/modulo_documento.py
"""

import io
import pytest
from fastapi import HTTPException, UploadFile

from services.modulo_documento import (
    get_modulo_documentos,
    get_modulo_documento,
    create_modulo_documento,
    update_modulo_documento,
    delete_modulo_documento,
)
from services.proyecto import create_proyecto
from services.modulo import create_modulo
from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from models.modulo_documento import ModuloDocumento


# ============================================================
# HELPERS
# ============================================================

def crear_proyecto_en_db(db, nombre="Proyecto X"):
    return create_proyecto(
        db,
        ProyectoCreate(
            nombre=nombre,
            objetivo_general="Objetivo",
            contexto="Contexto"
        )
    )


def crear_modulo_en_db(db, proyecto_id, nombre="Modulo X"):
    return create_modulo(
        db,
        ModuloCreate(
            proyecto_id=proyecto_id,
            nombre=nombre,
            tipo_interfaz="API",
            tipo_gui="web",
            descripcion="desc"
        )
    )


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
# MOCKS FILE SERVICE
# ============================================================

@pytest.fixture
def mock_save_file(monkeypatch):
    def fake_save(file, folder):
        return f"/fake/{folder}/{file.filename}"
    monkeypatch.setattr("services.modulo_documento.save_file", fake_save)


@pytest.fixture
def mock_replace_file(monkeypatch):
    def fake_replace(old, file, folder):
        return f"/fake/{folder}/new_{file.filename}"
    monkeypatch.setattr("services.modulo_documento.replace_file", fake_replace)


@pytest.fixture
def mock_delete_file(monkeypatch):
    monkeypatch.setattr("services.modulo_documento.delete_file", lambda x: None)


# ============================================================
# TESTS GET
# ============================================================

def test_get_modulo_documentos(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    crear_documento_en_db(db, m.id, "http://a.pdf")
    crear_documento_en_db(db, m.id, "http://b.pdf")

    docs = get_modulo_documentos(db)
    assert len(docs) == 2
    assert {d.archivo_url for d in docs} == {"http://a.pdf", "http://b.pdf"}


def test_get_modulo_documento_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    doc = crear_documento_en_db(db, m.id)

    resultado = get_modulo_documento(db, doc.id)
    assert resultado.id == doc.id
    assert resultado.archivo_url == doc.archivo_url


def test_get_modulo_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_modulo_documento(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Documento de módulo no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_modulo_documento(db, mock_save_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)

    file = UploadFile(filename="test.pdf", file=io.BytesIO(b"contenido"))

    doc = create_modulo_documento(db, m.id, file)

    assert doc.id is not None
    assert doc.modulo_id == m.id
    assert doc.archivo_url == "/fake/documentos_modulo/test.pdf"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_modulo_documento(db, mock_replace_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    doc = crear_documento_en_db(db, m.id, "http://old.pdf")

    new_file = UploadFile(filename="nuevo.pdf", file=io.BytesIO(b"nuevo"))

    actualizado = update_modulo_documento(db, doc.id, new_file)

    assert actualizado.archivo_url == "/fake/documentos_modulo/new_nuevo.pdf"


def test_update_modulo_documento_inexistente(db):
    new_file = UploadFile(filename="x.pdf", file=io.BytesIO(b"x"))

    with pytest.raises(HTTPException) as exc:
        update_modulo_documento(db, 9999, new_file)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_modulo_documento(db, mock_delete_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    doc = crear_documento_en_db(db, m.id)

    delete_modulo_documento(db, doc.id)

    with pytest.raises(HTTPException):
        get_modulo_documento(db, doc.id)


def test_delete_modulo_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_modulo_documento(db, 9999)

    assert exc.value.status_code == 404
