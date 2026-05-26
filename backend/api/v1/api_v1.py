from fastapi import APIRouter

# ============================================================
#  ARCHIVO PRINCIPAL DE RUTEO DE LA API (VERSIÓN /api/v1)
# ------------------------------------------------------------
#  Este archivo centraliza TODOS los routers del sistema.
#  Si un router NO se incluye aquí → NO aparece en Swagger.
# ============================================================


# -----------------------------
#  AUTENTICACIÓN
# -----------------------------
from api.v1.auth import router as auth_router


# -----------------------------
#  USUARIOS Y ROLES
# -----------------------------
from routes.usuario import router as usuario_router
from routes.rol import router as rol_router
from routes.usuario_rol import router as usuario_rol_router


# -----------------------------
#  SEGURIDAD (PERMISOS)
# -----------------------------
from routes.permiso import router as permiso_router
from routes.rol_permiso import router as rol_permiso_router


# -----------------------------
#  PROYECTO Y MÓDULOS
# -----------------------------
from routes.proyecto import router as proyecto_router
from routes.modulo import router as modulo_router
from routes.modulo_documento import router as modulo_documento_router
from routes.proyecto_documento import router as proyecto_documento_router


# -----------------------------
#  CASOS DE PRUEBA
# -----------------------------
from routes.caso_prueba import router as caso_prueba_router
from routes.caso_prueba_version import router as caso_prueba_version_router
from routes.paso import router as paso_router
from routes.paso_documento import router as paso_documento_router
from routes.paso_assert import router as paso_assert_router   # ← AGREGADO


# -----------------------------
#  EJECUCIONES
# -----------------------------
from routes.ejecucion import router as ejecucion_router
from routes.ejecucion_paso import router as ejecucion_paso_router
from routes.comentario import router as comentario_router


# -----------------------------
#  API Y PARÁMETROS
# -----------------------------
from routes.my_api import router as test_api_router
from routes.objeto_parametro import router as objeto_parametro_router


# -----------------------------
#  AUDITORIA
# -----------------------------
from routes import auditoria


# -----------------------------
#  AGENTES
# -----------------------------
from routes import agente


# ============================================================
#  MODELO INSTITUCIONAL (NUEVO)
# ============================================================
from routes.reparticion import router as reparticion_router
from routes.direccion import router as direccion_router
from routes.area import router as area_router


# ============================================================
#  ROUTER PRINCIPAL (VERSIÓN /api/v1)
# ============================================================
main_router = APIRouter(prefix="/api/v1")


# -----------------------------
#  AUTENTICACIÓN
# -----------------------------
main_router.include_router(auth_router)


# -----------------------------
#  USUARIOS Y ROLES
# -----------------------------
main_router.include_router(usuario_router)
main_router.include_router(rol_router)
main_router.include_router(usuario_rol_router)


# -----------------------------
#  SEGURIDAD (PERMISOS)
# -----------------------------
main_router.include_router(permiso_router)
main_router.include_router(rol_permiso_router)


# -----------------------------
#  PROYECTO Y MÓDULOS
# -----------------------------
main_router.include_router(proyecto_router)
main_router.include_router(modulo_router)
main_router.include_router(modulo_documento_router)
main_router.include_router(proyecto_documento_router)


# -----------------------------
#  CASOS DE PRUEBA
# -----------------------------
main_router.include_router(caso_prueba_router)
main_router.include_router(caso_prueba_version_router)
main_router.include_router(paso_router)
main_router.include_router(paso_documento_router)
main_router.include_router(paso_assert_router)   # ← AGREGADO


# -----------------------------
#  EJECUCIONES
# -----------------------------
main_router.include_router(ejecucion_router)
main_router.include_router(ejecucion_paso_router)
main_router.include_router(comentario_router)


# -----------------------------
#  API Y PARÁMETROS
# -----------------------------
main_router.include_router(test_api_router)
main_router.include_router(objeto_parametro_router)


# -----------------------------
#  AUDITORIA
# -----------------------------
main_router.include_router(auditoria.router)


# -----------------------------
#  AGENTES
# -----------------------------
main_router.include_router(agente.router)


# -----------------------------
#  MODELO INSTITUCIONAL (NUEVO)
# -----------------------------
main_router.include_router(reparticion_router)
main_router.include_router(direccion_router)
main_router.include_router(area_router)
