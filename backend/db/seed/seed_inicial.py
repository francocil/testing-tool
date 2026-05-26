"""
Seed institucional del sistema:
- Crea permisos institucionales (plural, alineados al SRS)
- Crea roles institucionales
- Asigna permisos a roles
- Crea usuario administrador inicial
"""

import models  # fuerza carga de modelos

from sqlalchemy.orm import Session
from db.session import SessionLocal

from models.permiso import Permiso
from models.rol import Rol
from models.rol_permiso import RolPermiso
from models.usuario import Usuario
from models.usuario_rol import UsuarioRol

from core.security import hash_password


# ============================================================
# PERMISOS INSTITUCIONALES (SRS + FRONTEND + BACKEND)
# ============================================================

PERMISOS = [

    # --- Dashboard ---
    "ver_dashboard",

    # --- Administración ---
    "admin_dashboard",
    "admin_agentes",
    "admin_parametros",

    # --- Proyectos ---
    "ver_proyectos",
    "crear_proyectos",
    "editar_proyectos",
    "eliminar_proyectos",
    "asignar_proyectos",
    "configurar_proyectos",

    # --- Módulos ---
    "ver_modulos",
    "crear_modulos",
    "editar_modulos",
    "eliminar_modulos",

    # --- Casos ---
    "ver_casos",
    "crear_casos",
    "editar_casos",
    "eliminar_casos",
    "versionar_casos",

    # --- Pasos ---
    "ver_pasos",
    "crear_pasos",
    "editar_pasos",
    "eliminar_pasos",

    # --- Parametro ---
    "ver_parametros",
    "crear_parametros",
    "editar_parametros",
    "eliminar_parametros",

    # --- Documentos ---
    "ver_documentos",
    "crear_documentos",
    "eliminar_documentos",

    # --- Ejecuciones ---
    "ver_ejecuciones",
    "crear_ejecuciones",
    "ejecutar_ejecuciones",
    "ejecutar_pasos_manual",
    "eliminar_ejecuciones",

    # --- Organigrama ---
    "ver_organigrama",
    "crear_reparticion",
    "editar_reparticion",
    "eliminar_reparticion",
    "crear_direccion",
    "editar_direccion",
    "eliminar_direccion",
    "crear_area",
    "editar_area",
    "eliminar_area",

    # --- Seguridad ---
    "ver_roles",
    "crear_roles",
    "editar_roles",
    "eliminar_roles",
    "ver_permisos",
    "asignar_permisos",
    "ver_usuario_roles",
    "asignar_usuario_roles",

    # --- Auditoría ---
    "ver_auditoria",
    "exportar_auditoria",

    # ============================================================
    # 🔥 MÓDULO APIs (COMPLETO)
    # ============================================================

    # CRUD APIs
    "ver_apis",
    "crear_apis",
    "editar_apis",
    "eliminar_apis",

    # Tester
    "probar_apis",

    # Versionado
    "ver_versiones_apis",
    "crear_versiones_apis",
    "editar_versiones_apis",
    "eliminar_versiones_apis",
    "clonar_versiones_apis",
    "restaurar_versiones_apis",
    "exportar_versiones_apis",

    # Superpermiso
    "admin_apis",
]


# ============================================================
# ROLES INSTITUCIONALES
# ============================================================

ROLES = {
    "ADMINISTRADOR": PERMISOS,  # tiene todo

    "RESPONSABLE_AREA": [
        "ver_dashboard",
        "ver_proyectos",
        "crear_proyectos",
        "editar_proyectos",
        "ver_modulos",
        "crear_modulos",
        "editar_modulos",
        "ver_casos",
        "crear_casos",
        "editar_casos",
        "ver_pasos",
        "crear_pasos",
        "editar_pasos",
        "ver_parametros",
        "crear_parametros",
        "editar_parametros",
        "eliminar_parametros",
        "ver_ejecuciones",
        "crear_ejecuciones",
        "ejecutar_ejecuciones",
        "ejecutar_pasos_manual",
        "ver_documentos",
        "crear_documentos",
        "eliminar_documentos",

        # APIs
        "ver_apis",
        "probar_apis",
        "ver_versiones_apis",
    ],

    "TESTER": [
        "ver_dashboard",
        "ver_proyectos",
        "ver_modulos",
        "ver_casos",
        "ver_pasos",
        "ver_documentos",
        "ver_ejecuciones",
        "crear_ejecuciones",
        "ejecutar_ejecuciones",
        "ejecutar_pasos_manual",

        # APIs
        "ver_apis",
        "probar_apis",
        "ver_versiones_apis",
    ],

    "DESARROLLADOR": [
        "ver_dashboard",
        "ver_proyectos",
        "ver_modulos",
        "ver_casos",
        "ver_pasos",
        "ver_documentos",

        # APIs (developer completo)
        "ver_apis",
        "crear_apis",
        "editar_apis",
        "eliminar_apis",
        "probar_apis",
        "ver_versiones_apis",
        "crear_versiones_apis",
        "editar_versiones_apis",
        "clonar_versiones_apis",
        "restaurar_versiones_apis",
        "exportar_versiones_apis",
    ],

    "VISOR": [
        "ver_dashboard",
        "ver_proyectos",
        "ver_modulos",
        "ver_casos",
        "ver_pasos",
        "ver_documentos",
        "ver_ejecuciones",

        # APIs
        "ver_apis",
        "ver_versiones_apis",
    ],
}


# ============================================================
# HELPERS
# ============================================================

def generar_descripcion(nombre: str) -> str:
    return nombre.replace("_", " ").capitalize()


# ============================================================
# SEED PRINCIPAL
# ============================================================

def run_seed():
    db: Session = SessionLocal()

    print("==> Creando permisos institucionales...")
    for nombre in PERMISOS:
        permiso = db.query(Permiso).filter_by(nombre=nombre).first()
        if not permiso:
            db.add(
                Permiso(
                    nombre=nombre,
                    descripcion=generar_descripcion(nombre),
                    activo=True
                )
            )
    db.commit()

    print("==> Creando roles institucionales...")
    roles_creados = {}
    for rol_nombre in ROLES.keys():
        rol = db.query(Rol).filter_by(nombre=rol_nombre).first()
        if not rol:
            rol = Rol(nombre=rol_nombre)
            db.add(rol)
            db.commit()
        roles_creados[rol_nombre] = rol

    print("==> Asignando permisos a roles...")
    for rol_nombre, permisos in ROLES.items():
        rol = roles_creados[rol_nombre]

        for permiso_nombre in permisos:
            permiso = db.query(Permiso).filter_by(nombre=permiso_nombre).first()
            if not permiso:
                continue

            existe = db.query(RolPermiso).filter_by(
                rol_id=rol.id,
                permiso_id=permiso.id
            ).first()

            if not existe:
                db.add(RolPermiso(rol_id=rol.id, permiso_id=permiso.id))

    db.commit()

    print("==> Creando usuario administrador inicial...")
    admin = db.query(Usuario).filter_by(email="admin@local.com").first()

    if not admin:
        admin = Usuario(
            nombre="Administrador",
            email="admin@local.com",
            password_hash=hash_password("admin123"),
            activo=True,
        )
        db.add(admin)
        db.commit()

        db.add(
            UsuarioRol(
                usuario_id=admin.id,
                rol_id=roles_creados["ADMINISTRADOR"].id
            )
        )
        db.commit()

    print("==> SEED INSTITUCIONAL COMPLETO ✔")


if __name__ == "__main__":
    run_seed()
