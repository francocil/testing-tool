// ============================================================
//  REQUIRE PERMISSION - PROTECCIÓN POR PERMISO
// ============================================================
//
// Uso:
//
// <RequirePermission permiso="ver_dashboard">
//     <Dashboard />
// </RequirePermission>
//
// Si el usuario NO tiene el permiso → unauthorized
//
// ============================================================

 import { Navigate } from "react-router-dom";
 import { usePermission } from "../../context/PermissionContext";

 export default function RequirePermission({ permiso, children }) {
   //const permisos = usePermission();
   const { permisos } = usePermission();


   // Si no hay permisos cargados, no permitir
   if (!permisos || permisos.length === 0) {
     return <Navigate to="/unauthorized" replace />;
   }

   // Si el usuario NO tiene el permiso → bloquear
   if (!permisos.includes(permiso)) {
     return <Navigate to="/unauthorized" replace />;
   }

   return children;
 }
