// ============================================================
//  PERMISSION CONTEXT - SISTEMA DE PERMISOS INSTITUCIONAL
// ============================================================

import { createContext, useContext, useMemo } from "react";
import { useSelector } from "react-redux";

// ------------------------------------------------------------
// 1) Crear contexto
// ------------------------------------------------------------
const PermissionContext = createContext({
  user: null,
  roles: [],
  permisos: [],
  loading: false,
  can: () => false,
  hasRole: () => false,
});

// ------------------------------------------------------------
// 2) Provider principal
// ------------------------------------------------------------
export function PermissionProvider({ children }) {
  const { user, isAuthenticated } = useSelector((state) => state.auth);

  const roles = useMemo(
    () => user?.roles?.map((r) => r.nombre) || [],
    [user]
  );

  const permisos = useMemo(
    () => user?.permisos || [],
    [user]
  );

  const can = (permiso) => permisos.includes(permiso);

  const hasRole = (rol) => roles.includes(rol);

  const value = useMemo(
    () => ({
      user,
      roles,
      permisos,
      loading: false,
      can,
      hasRole,
      isAuthenticated,
    }),
    [user, roles, permisos, isAuthenticated]
  );

  return (
    <PermissionContext.Provider value={value}>
      {children}
    </PermissionContext.Provider>
  );
}

// ------------------------------------------------------------
// 3) Hook para consultar permisos
// ------------------------------------------------------------
export function usePermission() {
  return useContext(PermissionContext);
}
