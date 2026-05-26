# my_tables.py

from pathlib import Path
from sqlalchemy import create_engine, text

# =========================================================
# CONFIGURACION
# =========================================================

DATABASE_URL = "postgresql+psycopg2://postgres:P$assword@localhost:5432/testing_tool"

# Archivo de salida
OUTPUT_FILE = "EstructuraDeTablas.txt"

# =========================================================
# CONEXION
# =========================================================

engine = create_engine(DATABASE_URL)

# =========================================================
# QUERY
# =========================================================

QUERY = """
SELECT
    c.table_schema,
    c.table_name,
    c.column_name,
    c.data_type,
    c.is_nullable,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale
FROM information_schema.columns c
WHERE c.table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY c.table_schema, c.table_name, c.ordinal_position;
"""

# =========================================================
# GENERAR ESTRUCTURA
# =========================================================

def generar_estructura():
    output_path = Path(OUTPUT_FILE)

    with engine.connect() as conn:
        result = conn.execute(text(QUERY))
        rows = result.fetchall()

    estructura = []
    tabla_actual = None

    for row in rows:
        schema = row.table_schema
        tabla = row.table_name
        columna = row.column_name
        tipo = row.data_type
        nullable = row.is_nullable

        max_length = row.character_maximum_length
        precision = row.numeric_precision
        scale = row.numeric_scale

        nombre_tabla_completo = f"{schema}.{tabla}"

        # Nueva tabla
        if tabla_actual != nombre_tabla_completo:
            estructura.append("\n" + "=" * 80)
            estructura.append(f"TABLA: {nombre_tabla_completo}")
            estructura.append("=" * 80)

            estructura.append(
                f"{'COLUMNA':30} {'TIPO':25} {'NULLABLE':10} {'DETALLE'}"
            )

            estructura.append("-" * 80)

            tabla_actual = nombre_tabla_completo

        # Detalles extra
        detalle = ""

        if max_length:
            detalle = f"length={max_length}"

        elif precision:
            detalle = f"precision={precision}"

            if scale is not None:
                detalle += f", scale={scale}"

        estructura.append(
            f"{columna:30} {tipo:25} {nullable:10} {detalle}"
        )

    # Guardar archivo
    output_path.write_text(
        "\n".join(estructura),
        encoding="utf-8"
    )

    print(f"\nOK - Archivo generado/actualizado: {output_path.resolve()}")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    generar_estructura()