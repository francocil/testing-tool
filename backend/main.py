from fastapi import FastAPI
from api.v1.api_v1 import main_router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from core.audit_middleware import AuditoriaMiddleware

load_dotenv()

app = FastAPI(
    title="Testing Tool API",
    version="1.0.0",
    description="Backend institucional para la herramienta de testing automatizado"
)

# ============================================================
# CORS — HABILITAR FRONTEND VITE (localhost y 127.0.0.1)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# HEALTH CHECK
# ============================================================
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ============================================================
# ROUTERS PRINCIPALES
# ============================================================
# El router ya tiene prefix="/api/v1"
app.include_router(api_router)

# ============================================================
# ARCHIVOS ESTÁTICOS (UPLOADS)
# ============================================================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ============================================================
# AUDITORÍA (DEBE IR AL FINAL)
# ============================================================
app.add_middleware(AuditoriaMiddleware)
