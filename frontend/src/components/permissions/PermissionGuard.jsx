// ============================================================
//  PERMISSION GUARD - CONTROL DE ACCESO INSTITUCIONAL
// ============================================================
//
// Responsabilidad:
// - Verificar permisos y roles del usuario.
// - Integrarse con PermissionContext (can, hasRole).
// - Evitar loops de navegación.
// - Proveer fallback automático a /unauthorized.
// - Permitir permisos múltiples (ALL o ANY).
//
// Uso:
//   <PermissionGuard permiso="ver_proyectos">
//       <Componente />
//   </PermissionGuard>
//
//   <PermissionGuard permisos={["editar_proyectos", "crear_proyectos"]} mode="any">
//       <Boton />
//   </PermissionGuard>
//
//   <PermissionGuard roles={["ADMINISTRADOR"]}>
//       <AdminPanel />
//   </PermissionGuard>
//
// ============================================================

import { Navigate } from "react-router-dom";
import { usePermission } from "../../context/PermissionContext";

const PermissionGuard = ({
  permiso = null,
  permisos = [],
  roles = [],
  mode = "all", // "all" = requiere todos, "any" = requiere alguno
  children,
}) => {
  const { loading, can, hasRole } = usePermission();

  // Mientras carga el usuario, no decidir todavía
  if (loading) {
    return <div>Cargando permisos...</div>;
  }

  // ------------------------------------------------------------
  // 1) Validar roles (si se especificaron)
  // ------------------------------------------------------------
  if (roles.length > 0) {
    const tieneRol = roles.some((r) => hasRole(r));
    if (!tieneRol) {
      return <Navigate to="/unauthorized" replace />;
    }
  }

  // ------------------------------------------------------------
  // 2) Validar permisos individuales
  // ------------------------------------------------------------
  if (permiso && !can(permiso)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // ------------------------------------------------------------
  // 3) Validar permisos múltiples
  // ------------------------------------------------------------
  if (permisos.length > 0) {
    if (mode === "all") {
      const ok = permisos.every((p) => can(p));
      if (!ok) return <Navigate to="/unauthorized" replace />;
    } else if (mode === "any") {
      const ok = permisos.some((p) => can(p));
      if (!ok) return <Navigate to="/unauthorized" replace />;
    }
  }

  return children;
};

export default PermissionGuard;
