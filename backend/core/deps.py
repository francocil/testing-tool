from sqlalchemy.orm import Session
from db.session import SessionLocal

# ============================================================
#  SESIÓN DE BASE DE DATOS
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
