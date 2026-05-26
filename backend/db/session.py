from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from collections.abc import Generator
from pathlib import Path
import os

# ---------------------------------------------------------
# Cargar variables de entorno desde backend/.env
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # carpeta backend
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")
#print(">>> DATABASE_URL:", DATABASE_URL)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# ---------------------------------------------------------
# Crear engine
# ---------------------------------------------------------
engine = create_engine(DATABASE_URL)

# ---------------------------------------------------------
# Crear SessionLocal
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# Dependencia para FastAPI
# ---------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
