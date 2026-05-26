// ============================================================
//  PROTECTED ROUTE INSTITUCIONAL
// ============================================================
//
// - Verifica token
// - Verifica isAuthenticated
// - Espera a que Redux termine de cargar
// - Redirige correctamente
//
// ============================================================

import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const { token, isAuthenticated, status } = useSelector(
    (state) => state.auth
  );

  // ⏳ Mientras Redux está cargando el usuario (/auth/me)
  if (status === "loading") {
    return null; // o un spinner si querés
  }

  // ❌ No hay token → no está logueado
  if (!token || !isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // ✔ Usuario autenticado
  return children;
}
