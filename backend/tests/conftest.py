#================================================================================
# CONFIGURACIÓN DE TESTING PARA FASTAPI + SQLITE EN MEMORIA
#================================================================================#
# Este archivo:
# 1) Crea una base SQLite en memoria (rápida, aislada, sin tocar tu base real).
# 2) Crea una sesión por test (tablas limpias en cada test).
# 3) Sobrescribe get_db para que FastAPI use la DB de test.
# 4) Crea un TestClient para llamar a tus rutas como un cliente real.
# 5) Sobrescribe TODAS las dependencias de autenticación:
#       - get_current_user
#       - TODAS las funciones internas role_checker generadas por require_role
#
# Esto es CRÍTICO porque:
# - require_role(...) genera funciones internas dinámicas (role_checker)
# - FastAPI registra esas funciones, NO require_role
# - Por eso mockear require_role NO funciona
# - Y role_checker espera un Usuario SQLAlchemy → rompe SQLite por threads
# - Y si devolvés un dict → rompe porque accede a user.rol_id
#
# Este archivo resuelve TODO eso.
#================================================================================

import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.routing import APIRoute

from main import app
from db.base import Base
from db.session import get_db, SessionLocal
from core.auth import get_current_user


# ============================================================
# ENGINE GLOBAL (ARCHIVO TEMPORAL SQLITE)
# ============================================================

@pytest.fixture(scope="session")
def engine():
    """
    En Windows NO funciona sqlite:///:memory: con múltiples conexiones.
    Por eso usamos un archivo temporal SQLite.
    """
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()

    test_engine = create_engine(
        f"sqlite:///{temp_db.name}",
        echo=False,
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(bind=test_engine)

    # Reemplazar el engine real por el engine de test
    SessionLocal.configure(bind=test_engine)

    return test_engine


# ============================================================
# SESIÓN POR TEST
# ============================================================

@pytest.fixture
def db(engine):
    """
    Limpia y recrea las tablas antes de cada test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


# ============================================================
# MOCK DE AUTENTICACIÓN Y ROLES
# ============================================================

@pytest.fixture(autouse=True)
def mock_auth():
    """
    Neutraliza TODA la autenticación y autorización.
    """

    fake_user_obj = {
        "id": 1,
        "rol_id": 1,
        "nombre": "Test User",
        "email": "test@example.com"
    }

    # Mock de get_current_user
    app.dependency_overrides[get_current_user] = lambda: fake_user_obj

    # Mock de role_checker
    def fake_role_checker():
        return True

    # Reemplazar TODAS las funciones role_checker registradas
    for route in app.routes:
        if isinstance(route, APIRoute):
            for dep in route.dependant.dependencies:
                if dep.call and dep.call.__name__ == "role_checker":
                    app.dependency_overrides[dep.call] = fake_role_checker

    yield
    app.dependency_overrides.clear()


# ============================================================
# CLIENTE FASTAPI
# ============================================================

@pytest.fixture
def client(db):
    """
    TestClient usando la DB de test.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
