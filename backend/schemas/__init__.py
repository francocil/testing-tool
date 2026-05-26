# -----------------------------
# Proyectos
# -----------------------------
from .proyecto import (
    ProyectoBase,
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse,
)

from .proyecto_documento import (
    ProyectoDocumentoBase,
    ProyectoDocumentoCreate,
    ProyectoDocumentoUpdate,
    ProyectoDocumentoResponse,
)


# -----------------------------
# Módulos
# -----------------------------
from .modulo import (
    ModuloBase,
    ModuloCreate,
    ModuloUpdate,
    Modulo,   # ← CORRECTO
)

from .modulo_documento import (
    ModuloDocumentoBase,
    ModuloDocumentoCreate,
    ModuloDocumentoUpdate,
    ModuloDocumentoResponse,
)


# -----------------------------
# Casos de Prueba
# -----------------------------
from .caso_prueba import (
    CasoPruebaBase,
    CasoPruebaCreate,
    CasoPruebaUpdate,
    CasoPrueba,   # ← CORRECTO
)

from .caso_prueba_version import (
    CasoPruebaVersionBase,
    CasoPruebaVersionCreate,
    CasoPruebaVersionUpdate,
    CasoPruebaVersionResponse,
)


# -----------------------------
# Pasos
# -----------------------------
from .paso import (
    PasoBase,
    PasoCreate,
    PasoUpdate,
    Paso,   # ← CORRECTO
)

from .paso_documento import (
    PasoDocumentoBase,
    PasoDocumentoCreate,
    PasoDocumentoUpdate,
    PasoDocumentoResponse,
)


# -----------------------------
# Objetos / APIs
# -----------------------------
from .objeto_parametro import (
    ObjetoParametroBase,
    ObjetoParametroCreate,
    ObjetoParametroUpdate,
    ObjetoParametroResponse,
)

from .my_api import (
    ApiBase,
    ApiCreate,
    ApiUpdate,
    ApiResponse,
)


# -----------------------------
# Ejecuciones
# -----------------------------
from .ejecucion import (
    EjecucionBase,
    EjecucionCreate,
    EjecucionUpdate,
    Ejecucion,   # ← CORRECTO
)

from .ejecucion_paso import (
    EjecucionPasoBase,
    EjecucionPasoCreate,
    EjecucionPasoUpdate,
    EjecucionPaso,   # ← CORRECTO
)


# -----------------------------
# Comentarios
# -----------------------------
from .comentario import (
    ComentarioBase,
    ComentarioCreate,
    ComentarioUpdate,
    ComentarioResponse,
)


# -----------------------------
# Usuarios / Roles
# -----------------------------
from .usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)

from .rol import (
    RolBase,
    RolCreate,
    RolUpdate,
    RolResponse,
)


# -----------------------------
# Auth
# -----------------------------
from .auth import (
    LoginRequest,
    AuthUser,
    LoginResponse,
)
