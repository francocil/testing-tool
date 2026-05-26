"""
Tests para services/paso_documento.py

Cubre:
- get_paso_documentos
- get_paso_documento
- create_paso_documento
- update_paso_documento
- delete_paso_documento

Incluye:
- Mock de save_file, replace_file, delete_file
- Validación de FK a paso
- Manejo correcto de errores HTTP
"""

import io
import pytest
from fastapi import HTTPException, UploadFile

from services.paso_documento import (
    get_paso_documentos,
    get_paso_documento,
    create_paso_documento,
    update_paso_documento,
    delete_paso_documento,
)
from services.proyecto import create_proyecto
from services.modulo import create_modulo
from services.caso_prueba import create_caso_prueba
from services.paso import create_paso
from schemas.proyecto import ProyectoCreate
from schemas.modulo import ModuloCreate
from schemas.caso_prueba import CasoPruebaCreate
from schemas.paso import PasoCreate
from models.paso_documento import PasoDocumento


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


def crear_caso_en_db(db, modulo_id, nombre="Caso X"):
    return create_caso_prueba(
        db,
        CasoPruebaCreate(
            modulo_id=modulo_id,
            nombre=nombre,
            objetivo="Objetivo",
            porcentaje_aceptacion=80.0
        )
    )


def crear_paso_en_db(db, caso_id, orden=1, descripcion="Paso test"):
    return create_paso(
        db,
        PasoCreate(
            caso_id=caso_id,
            orden=orden,
            descripcion=descripcion
        )
    )


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
# MOCKS FILE SERVICE
# ============================================================

@pytest.fixture
def mock_save_file(monkeypatch):
    def fake_save(file, folder):
        return f"/fake/{folder}/{file.filename}"
    monkeypatch.setattr("services.paso_documento.save_file", fake_save)


@pytest.fixture
def mock_replace_file(monkeypatch):
    def fake_replace(old, file, folder):
        return f"/fake/{folder}/new_{file.filename}"
    monkeypatch.setattr("services.paso_documento.replace_file", fake_replace)


@pytest.fixture
def mock_delete_file(monkeypatch):
    monkeypatch.setattr("services.paso_documento.delete_file", lambda x: None)


# ============================================================
# TESTS GET
# ============================================================

def test_get_paso_documentos(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)

    crear_documento_en_db(db, paso.id, "http://a.pdf")
    crear_documento_en_db(db, paso.id, "http://b.pdf")

    docs = get_paso_documentos(db)
    assert len(docs) == 2
    assert {d.archivo_url for d in docs} == {"http://a.pdf", "http://b.pdf"}


def test_get_paso_documento_existente(db):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    doc = crear_documento_en_db(db, paso.id)

    resultado = get_paso_documento(db, doc.id)
    assert resultado.id == doc.id
    assert resultado.archivo_url == doc.archivo_url


def test_get_paso_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        get_paso_documento(db, 9999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Documento de paso no encontrado"


# ============================================================
# TESTS CREATE
# ============================================================

def test_create_paso_documento(db, mock_save_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)

    file = UploadFile(filename="test.pdf", file=io.BytesIO(b"contenido"))

    doc = create_paso_documento(db, paso.id, file)

    assert doc.id is not None
    assert doc.paso_id == paso.id
    assert doc.archivo_url == "/fake/documentos_paso/test.pdf"


# ============================================================
# TESTS UPDATE
# ============================================================

def test_update_paso_documento(db, mock_replace_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    doc = crear_documento_en_db(db, paso.id, "http://old.pdf")

    new_file = UploadFile(filename="nuevo.pdf", file=io.BytesIO(b"nuevo"))

    actualizado = update_paso_documento(db, doc.id, new_file)

    assert actualizado.archivo_url == "/fake/documentos_paso/new_nuevo.pdf"


def test_update_paso_documento_inexistente(db):
    new_file = UploadFile(filename="x.pdf", file=io.BytesIO(b"x"))

    with pytest.raises(HTTPException) as exc:
        update_paso_documento(db, 9999, new_file)

    assert exc.value.status_code == 404


# ============================================================
# TESTS DELETE
# ============================================================

def test_delete_paso_documento(db, mock_delete_file):
    p = crear_proyecto_en_db(db)
    m = crear_modulo_en_db(db, p.id)
    c = crear_caso_en_db(db, m.id)
    paso = crear_paso_en_db(db, c.id)
    doc = crear_documento_en_db(db, paso.id)

    delete_paso_documento(db, doc.id)

    with pytest.raises(HTTPException):
        get_paso_documento(db, doc.id)


def test_delete_paso_documento_inexistente(db):
    with pytest.raises(HTTPException) as exc:
        delete_paso_documento(db, 9999)

    assert exc.value.status_code == 404
