import os
import re

# Mapeo de nombres actuales → nombres normalizados
RENAMES = {
    # MODELS
    "api.py": "api.py",
    "caso_prueba.py": "caso_prueba.py",
    "caso_prueba_version.py": "caso_prueba_version.py",
    "comentario.py": "comentario.py",
    "ejecucion.py": "ejecucion.py",
    "ejecucion_paso.py": "ejecucion_paso.py",
    "modulo.py": "modulo.py",
    "modulo_documento.py": "modulo_documento.py",
    "objeto_parametro.py": "objeto_parametro.py",
    "paso.py": "paso.py",
    "paso_documento.py": "paso_documento.py",
    "proyecto.py": "proyecto.py",
    "proyecto_documento.py": "proyecto_documento.py",
    "rol.py": "rol.py",
    "usuario.py": "usuario.py",

    # SERVICES
    "caso_prueba_version.py": "caso_prueba_version.py",
    "modulo_documento.py": "modulo_documento.py",
    "paso_documento.py": "paso_documento.py",
    "proyecto_documento.py": "proyecto_documento.py",
}

# Carpetas a procesar
TARGET_DIRS = ["models", "schemas", "services"]

def rename_files():
    for folder in TARGET_DIRS:
        path = os.path.join(".", folder)
        for filename in os.listdir(path):
            if filename in RENAMES:
                old = os.path.join(path, filename)
                new = os.path.join(path, RENAMES[filename])
                print(f"Renombrando: {old} → {new}")
                os.rename(old, new)

def update_imports():
    pattern = re.compile(r"(from\s+models\.|from\s+schemas\.|from\s+services\.)(\w+)")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and "venv" not in root:
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                for old, new in RENAMES.items():
                    old_module = old.replace(".py", "")
                    new_module = new.replace(".py", "")
                    new_content = new_content.replace(old_module, new_module)

                if new_content != content:
                    print(f"Actualizando imports en: {full_path}")
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

if __name__ == "__main__":
    rename_files()
    update_imports()
    print("\nNormalización completada.")