// ============================================================
//  AUTH SLICE - AUTENTICACIÓN + ROLES/PERMISOS NORMALIZADOS
// ============================================================

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getCurrentUser } from "../api/auth";

// ------------------------------------------------------------
// 1) Mapeo de roles del backend → roles internos
// ------------------------------------------------------------
const roleMap = {
  Administrador: "admin",
  Admin: "admin",
  Tester: "tester",
  Developer: "developer",
  Usuario: "viewer",
};

// ------------------------------------------------------------
// 2) Normalizador de roles
// ------------------------------------------------------------
const normalizeRole = (rawRole) => {
  if (!rawRole) return "viewer";
  return roleMap[rawRole] || "viewer";
};

// ------------------------------------------------------------
// 3) Thunk: carga el usuario autenticado desde /auth/me
// ------------------------------------------------------------
// /auth/me devuelve:
// {
//   id,
//   nombre,
//   email,
//   activo,
//   fecha_creacion,
//   fecha_actualizacion,
//   roles: [{ id, nombre }],
//   permisos: [ "ver_proyectos", ... ]
// }
export const fetchCurrentUser = createAsyncThunk(
  "auth/fetchCurrentUser",
  async (_, { rejectWithValue }) => {
    try {
      const data = await getCurrentUser();
      return data; // usuario plano, NO envuelto en { usuario: ... }
    } catch (error) {
      return rejectWithValue(error.response?.data || "Error al obtener usuario");
    }
  }
);

// ------------------------------------------------------------
// 4) Estado inicial
// ------------------------------------------------------------
const initialState = {
  user: null,               // Siempre el objeto usuario plano
  role: null,               // Rol normalizado (admin/tester/viewer/etc.)
  token: localStorage.getItem("token") || null,
  refresh_token: localStorage.getItem("refresh_token") || null,
  isAuthenticated: !!localStorage.getItem("token"),
  status: "idle",
  error: null,
};

// ------------------------------------------------------------
// 5) Slice principal
// ------------------------------------------------------------
const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    // --------------------------------------------------------
    // LOGIN EXITOSO
    // --------------------------------------------------------
    // Backend /auth/login devuelve:
    // {
    //   access_token,
    //   refresh_token,
    //   usuario: {
    //     id,
    //     nombre,
    //     email,
    //     roles: [{ id, nombre }],
    //     permisos: [ "ver_proyectos", ... ]
    //   }
    // }
    loginSuccess: (state, action) => {
      const { access_token, refresh_token, usuario } = action.payload || {};

      const rawRole = usuario?.roles?.[0]?.nombre;
      const normalizedRole = normalizeRole(rawRole);

      state.token = access_token || null;
      state.refresh_token = refresh_token || null;

      // Usuario SIEMPRE plano, con roles y permisos
      state.user = usuario || null;
      state.role = normalizedRole;
      state.isAuthenticated = !!access_token;

      localStorage.setItem("token", access_token || "");
      if (refresh_token) {
        localStorage.setItem("refresh_token", refresh_token);
      }
    },

    // --------------------------------------------------------
    // LOGOUT
    // --------------------------------------------------------
    logout: (state) => {
      state.token = null;
      state.refresh_token = null;
      state.user = null;
      state.role = null;
      state.isAuthenticated = false;
      state.status = "idle";
      state.error = null;

      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
    },
  },

  // ------------------------------------------------------------
  // 6) Manejo de fetchCurrentUser
  // ------------------------------------------------------------
  extraReducers: (builder) => {
    builder
      .addCase(fetchCurrentUser.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })

      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        const usuario = action.payload || null;
        const rawRole = usuario?.roles?.[0]?.nombre;
        const normalizedRole = normalizeRole(rawRole);

        state.status = "idle";
        state.user = usuario;
        state.role = normalizedRole;
        state.isAuthenticated = true;
        state.error = null;
      })

      .addCase(fetchCurrentUser.rejected, (state) => {
        state.status = "idle";
        state.user = null;
        state.role = null;
        state.isAuthenticated = false;
        state.token = null;
        state.refresh_token = null;
        state.error = "No se pudo obtener el usuario actual";

        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
      });
  },
});

export const { loginSuccess, logout } = authSlice.actions;
export default authSlice.reducer;
