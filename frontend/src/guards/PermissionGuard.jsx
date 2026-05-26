// ============================================================
//  PERMISSION GUARD INSTITUCIONAL
// ============================================================
//
// - Usa PermissionContext
// - Espera loading
// - Verifica permiso con can()
// - Redirige a /unauthorized
//
// ============================================================

import { Navigate } from "react-router-dom";
import { usePermission } from "../context/PermissionContext";

export default function PermissionGuard({ permiso, children }) {
  const { can, loading } = usePermission();

  // ⏳ Mientras carga el usuario (/auth/me)
  if (loading) return null; // o un spinner si querés

  // ❌ No tiene permiso
  if (!can(permiso)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // ✔ Tiene permiso
  return children;
}
