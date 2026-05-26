// ============================================================
//  useAuth() - Hook institucional de autenticación
// ============================================================
//
// Este hook:
// - Lee el estado de auth desde Redux
// - Expone user, token, role, isAuthenticated, status
// - NO normaliza roles (ya lo hace el slice)
// - NO maneja permisos (eso es PermissionContext)
// ============================================================

import { useSelector } from "react-redux";

export default function useAuth() {
  const { user, token, role, isAuthenticated, status } = useSelector(
    (state) => state.auth
  );

  return {
    user,
    token,
    role,
    isAuthenticated,
    status,

    // Helpers institucionales
    isAdmin: role === "admin",
    isTester: role === "tester",
    isDeveloper: role === "developer",
    isViewer: role === "viewer",
  };
}
