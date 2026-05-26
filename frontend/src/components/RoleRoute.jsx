// ============================================================
//  ROLE ROUTE - PROTECCIÓN POR ROL (VERSIÓN ESTABLE)
// ============================================================
//
// Problema que resuelve:
// - Evita redirigir a /unauthorized mientras Redux todavía
//   está cargando el usuario y el rol.
// - Solo decide acceso cuando el estado está listo.
//
// Flujo:
//
// 1) status === "loading"  → mostrar "Cargando permisos...".
// 2) status === "idle"     → todavía no hay datos, esperar.
// 3) status === "failed"   → usuario inválido → unauthorized.
// 4) status === "succeeded":
//      - si !role → unauthorized
//      - si role NO está en allowed → unauthorized
//      - si role está permitido → renderiza children
//
// ============================================================

import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

export default function RoleRoute({ allowed, children }) {
  const { role, status } = useSelector((state) => state.auth);

  
  // Mientras Redux está cargando el usuario/rol, NO decidir.
  if (status === "loading" || status === "idle") {
    return <div>Cargando permisos...</div>;
  }

  // Si la carga del usuario falló, no hay permisos válidos.
  if (status === "failed") {
    return <Navigate to="/unauthorized" replace />;
  }

  // Si no hay rol una vez resuelto el estado, acceso denegado.
  if (!role) {
    return <Navigate to="/unauthorized" replace />;
  }

  // Comparación directa con el string del rol.
  if (!allowed.includes(role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}
