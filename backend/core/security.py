"""
Módulo de seguridad central del sistema.
Gestiona:
- Hashing y verificación de contraseñas
- Generación de tokens JWT (access y refresh)
- Decodificación segura de tokens
"""

import os
from datetime import datetime, timedelta
from typing import Optional, cast
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv


# ============================================================
# CARGA DEL ARCHIVO .env (siempre antes de leer variables)
# ============================================================

# Carga el .env desde la raíz del proyecto, independientemente del import order
load_dotenv()


# ============================================================
# VARIABLES DE ENTORNO (ya garantizadas)
# ============================================================

SECRET_KEY = cast(str, os.getenv("ACCESS_SECRET"))
REFRESH_SECRET_KEY = cast(str, os.getenv("REFRESH_SECRET"))

if not SECRET_KEY:
    raise RuntimeError("Falta ACCESS_SECRET en el archivo .env")

if not REFRESH_SECRET_KEY:
    raise RuntimeError("Falta REFRESH_SECRET en el archivo .env")


# ============================================================
# CONFIGURACIÓN JWT
# ============================================================

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================
# HASHING DE CONTRASEÑAS
# ============================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# GENERACIÓN DE TOKENS JWT
# ============================================================

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# DECODIFICACIÓN DE TOKENS
# ============================================================

def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def decode_refresh_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
