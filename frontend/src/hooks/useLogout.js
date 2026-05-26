// ============================================================
//  useLogout PRO - Limpieza total y segura
// ============================================================

import { useDispatch } from "react-redux";
import { logout } from "../store/authSlice";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function useLogout() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  return () => {
    // 1) Cancelar requests pendientes (incluye refresh)
    axios.defaults.cancelToken = axios.CancelToken.source();
    axios.defaults.cancelToken.cancel("Logout: cancelando requests");

    // 2) Limpiar Redux (incluye tokens y user)
    dispatch(logout());

    // 3) Redirigir sin historial
    navigate("/login", { replace: true });
  };
}
