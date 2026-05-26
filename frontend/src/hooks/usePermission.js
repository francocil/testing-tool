import { usePermission } from "../context/PermissionContext";   

// ------------------------------------------------------------
// Hook institucional para consultar permisos del usuario
// ------------------------------------------------------------

export default function usePermission() {
    const {
        permissions,
        loading,
        hasPermission,
        hasAnyPermission,
        hasAllPermissions,
    } = usePermissionContext();

    // Alias corto y elegante
    const can = hasPermission;

    return {
        permissions,
        loading,
        can,
        hasPermission,
        hasAnyPermission,
        hasAllPermissions,
    };
}
