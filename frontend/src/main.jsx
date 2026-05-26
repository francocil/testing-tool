// ============================================================
//  MAIN.JSX - THEME + REDUX + ROUTER PRINCIPAL
// ============================================================

import React, { createContext, useMemo, useState, useEffect } from "react";
import ReactDOM from "react-dom/client";

import { ThemeProvider } from "@mui/material/styles";
import { CssBaseline, useMediaQuery } from "@mui/material";
import { getTheme } from "./theme/theme.js";

import { Provider, useDispatch, useSelector } from "react-redux";
import { store } from "./store/store";

import AppRouter from "./router/AppRouter";
import { PermissionProvider } from "./context/PermissionContext";
import { fetchCurrentUser } from "./store/authSlice";

// ------------------------------------------------------------
// INITIALIZER - Carga /auth/me apenas hay token
// ------------------------------------------------------------
function Initializer() {
  const dispatch = useDispatch();
  const token = useSelector((state) => state.auth.token);

  useEffect(() => {
    if (token) {
      dispatch(fetchCurrentUser());
    }
  }, [token, dispatch]);

  return null;
}

// ------------------------------------------------------------
// THEME MODE CONTEXT
// ------------------------------------------------------------
export const ThemeModeContext = createContext({
  mode: "light",
  toggleMode: () => {},
});

// ------------------------------------------------------------
// THEME PROVIDER
// ------------------------------------------------------------
function AppThemeProvider({ children }) {
  const systemPrefersDark = useMediaQuery("(prefers-color-scheme: dark)");
  const storedMode = localStorage.getItem("themeMode");

  const [mode, setMode] = useState(
    storedMode || (systemPrefersDark ? "dark" : "light")
  );

  useEffect(() => {
    localStorage.setItem("themeMode", mode);
  }, [mode]);

  const toggleMode = () => {
    setMode((prev) => (prev === "light" ? "dark" : "light"));
  };

  const theme = useMemo(() => getTheme(mode), [mode]);

  return (
    <ThemeModeContext.Provider value={{ mode, toggleMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeModeContext.Provider>
  );
}

// ------------------------------------------------------------
// RENDER PRINCIPAL
// ------------------------------------------------------------
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <AppThemeProvider>

        {/* Carga /auth/me apenas hay token */}
        <Initializer />

        {/* PermissionProvider envuelve SOLO lo que necesita permisos */}
        <PermissionProvider>
          <AppRouter />
        </PermissionProvider>

      </AppThemeProvider>
    </Provider>
  </React.StrictMode>
);
