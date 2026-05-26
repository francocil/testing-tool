from pathlib import Path

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Ruta raíz desde donde generar el árbol
ROOT_DIR = Path(".")

# Archivo de salida
OUTPUT_FILE = "Estructura.txt"

# ------------------------------------------------------------
# EXCLUSIONES
# ------------------------------------------------------------

# Carpetas a excluir COMPLETAMENTE
# (no aparecen ni la carpeta ni su contenido)
EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "dist",
    "build",
}

# Carpetas cuyo CONTENIDO querés ocultar
# (la carpeta aparece, pero no lo que tiene adentro)
HIDE_CONTENT_OF_DIRS = {
    "logs",
    "uploads",
    "media",
    "node_modules",
    "venv",
}

# Archivos a excluir
EXCLUDED_FILES = {
    ".env",
    "package-lock.json",
}

# Extensiones de archivos a excluir
EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".log",
}


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def generate_tree(path: Path, prefix: str = "") -> list[str]:
    lines = []

    try:
        items = sorted(
            path.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower())
        )
    except PermissionError:
        return [prefix + "└── [Acceso denegado]"]

    # Filtrar elementos excluidos
    filtered_items = []

    for item in items:

        # Excluir carpetas completas
        if item.is_dir() and item.name in EXCLUDED_DIRS:
            continue

        # Excluir archivos específicos
        if item.is_file() and item.name in EXCLUDED_FILES:
            continue

        # Excluir extensiones
        if item.is_file() and item.suffix in EXCLUDED_EXTENSIONS:
            continue

        filtered_items.append(item)

    # Construcción visual del árbol
    for index, item in enumerate(filtered_items):
        is_last = index == len(filtered_items) - 1

        connector = "└── " if is_last else "├── "

        lines.append(prefix + connector + item.name)

        # Si es carpeta
        if item.is_dir():

            # Mostrar carpeta pero ocultar contenido
            if item.name in HIDE_CONTENT_OF_DIRS:
                hidden_prefix = "    " if is_last else "│   "
                lines.append(prefix + hidden_prefix + "└── [contenido oculto]")
                continue

            extension = "    " if is_last else "│   "

            lines.extend(
                generate_tree(
                    item,
                    prefix + extension
                )
            )

    return lines


# ============================================================
# EJECUCIÓN
# ============================================================

def main():
    root_name = ROOT_DIR.resolve().name

    tree_lines = [root_name]
    tree_lines.extend(generate_tree(ROOT_DIR))

    tree_text = "\n".join(tree_lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(tree_text)

    print(f"\n✔ Árbol generado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()