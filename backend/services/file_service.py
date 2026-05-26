import os
import uuid
import shutil
from fastapi import UploadFile

# ============================================================
# BASE_DIR
# ------------------------------------------------------------
# Directorio raíz REAL del backend.
# Si este archivo está en:
#   backend/services/file_service.py
#
# Entonces BASE_DIR apunta a:
#   backend/
#
# Esto es CRÍTICO porque:
# - Las rutas relativas deben generarse respecto al backend.
# - El router de descarga usa os.getcwd() (que es backend/).
# - Evita rutas como "../uploads/..." que rompen la descarga.
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ============================================================
# BASE_UPLOAD_DIR
# ------------------------------------------------------------
# Carpeta absoluta donde se guardan los archivos subidos.
# Queda así:
#   backend/uploads/
#
# Todas las subcarpetas (documentos_paso, documentos_modulo, etc.)
# se crean dentro de esta carpeta.
# ============================================================
BASE_UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


# ============================================================
# ensure_directory
# ------------------------------------------------------------
# Crea una carpeta si no existe.
# Evita errores al guardar archivos.
# ============================================================
def ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)


# ============================================================
# save_file
# ------------------------------------------------------------
# Guarda un archivo físico en:
#   backend/uploads/<folder>/
#
# Y devuelve SIEMPRE una ruta RELATIVA respecto a backend/, por ejemplo:
#   uploads/documentos_paso/uuid_nombre.pdf
#
# Esto garantiza compatibilidad con:
# - FileResponse
# - os.getcwd()
# - Windows y Linux
# ============================================================
def save_file(file: UploadFile, folder: str = "") -> str:
    directory = os.path.join(BASE_UPLOAD_DIR, folder)
    ensure_directory(directory)

    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ruta relativa respecto a backend/
    relative_path = os.path.relpath(filepath, BASE_DIR)
    return relative_path.replace("\\", "/")


# ============================================================
# delete_file
# ------------------------------------------------------------
# Elimina un archivo físico.
# Acepta rutas:
# - Absolutas
# - Relativas respecto a backend/
#
# Esto permite borrar archivos antiguos sin importar cómo se guardaron.
# ============================================================
def delete_file(filepath: str):
    if not filepath:
        return

    if not os.path.isabs(filepath):
        filepath = os.path.join(BASE_DIR, filepath)

    if os.path.exists(filepath):
        os.remove(filepath)


# ============================================================
# replace_file
# ------------------------------------------------------------
# Borra el archivo anterior y guarda uno nuevo.
# Devuelve SIEMPRE una ruta relativa respecto a backend/.
# ============================================================
def replace_file(old_path: str, new_file: UploadFile, folder: str = "") -> str:
    delete_file(old_path)
    return save_file(new_file, folder)
