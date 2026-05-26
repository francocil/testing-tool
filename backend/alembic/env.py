from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from db.base import Base

# ---------------------------------------------------------
# 🔥 IMPORTAR TODOS LOS MODELOS (CRÍTICO)
# ---------------------------------------------------------

# Modelos existentes
from models import (
    my_api,
    rol,
    rol_permiso,
    usuario,
    proyecto,
    usuario_proyecto,
    proyecto_documento,
    modulo,
    modulo_documento,
    caso_prueba,
    caso_prueba_version,
    paso,
    paso_documento,
    objeto_parametro,
    ejecucion,
    ejecucion_paso,
    comentario,
)

# 👇 AGREGÁ ESTOS (faltaban)
from models.agente import Agente
from models.reparticion import Reparticion
from models.area import Area
from models.direccion import Direccion
from models.permiso import Permiso
from models.rol_permiso import RolPermiso

# ---------------------------------------------------------
# Configuración de Alembic
# ---------------------------------------------------------
config = context.config

config.set_main_option(
    "sqlalchemy.url",
    "postgresql+psycopg2://postgres:P$assword@localhost:5432/testing_tool"
)

# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------
target_metadata = Base.metadata

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    ini_section = config.get_section(config.config_ini_section)
    if ini_section is None:
        ini_section = {}

    connectable = engine_from_config(
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()