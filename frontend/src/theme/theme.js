// ============================================================
//  THEME INSTITUCIONAL - GOBIERNO DE TUCUMÁN (2024)
// ============================================================
//
// Este theme está construido siguiendo el Manual de Marca 2024:
// - Paleta cromática oficial (Azul, Celeste, Blanco, Amarillo)
// - Tipografía corporativa Roboto (sustituto accesible de Gotham)
// - Iconografía Material Icons (según manual)
// - Proporción cromática y accesibilidad
//
// Además incluye:
// - Modo claro/oscuro automático según configuración del sistema
// - Overrides institucionales para AppBar, Paper y Buttons
// - Transiciones suaves y diseño moderno
//
// Para usarlo, envolver la app con <ThemeProvider theme={getTheme(...)}>.
// ============================================================

import { createTheme } from "@mui/material/styles";

// ------------------------------------------------------------
// ⭐ DETECCIÓN AUTOMÁTICA DEL MODO DEL SISTEMA OPERATIVO
// ------------------------------------------------------------
// Si el usuario tiene el sistema en modo oscuro → "dark"
// Si lo tiene en modo claro → "light"
// Esto permite que la app siga la preferencia del SO.
export const systemMode =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";

// ------------------------------------------------------------
// 1) Colores institucionales según Manual de Marca 2024
// ------------------------------------------------------------
const colors = {
  azul: "#005CA2",     // Azul institucional (color principal)
  celeste: "#84CFED",  // Celeste institucional (apoyo)
  blanco: "#FFFFFF",   // Blanco (fondo y contraste)
  amarillo: "#FEC800", // Amarillo institucional (destacados)
};

// ------------------------------------------------------------
// 2) Función que genera el theme dinámicamente
//    Permite cambiar entre modo claro y oscuro
//    ⭐ Ahora soporta modo automático usando systemMode
// ------------------------------------------------------------
export const getTheme = (mode = systemMode) =>
  createTheme({
    // --------------------------------------------------------
    // 3) PALETA DE COLORES
    // --------------------------------------------------------
    palette: {
      mode, // "light" o "dark"

      // Colores principales institucionales
      primary: {
        main: colors.azul,
        light: colors.celeste,
        contrastText: colors.blanco,
      },

      // Amarillo institucional para destacar elementos
      secondary: {
        main: colors.amarillo,
        contrastText: "#000000",
      },

      // Fondos según modo claro/oscuro
      background: {
        default: mode === "light" ? "#FFFFFF" : "#0A0A0A",
        paper: mode === "light" ? "#FFFFFF" : "#121212",
      },

      // Texto accesible según modo
      text: {
        primary: mode === "light" ? "#1A1A1A" : "#FFFFFF",
        secondary: mode === "light" ? "#4A4A4A" : "#CCCCCC",
      },

      // Estados
      success: { main: "#2E7D32" },
      error: { main: "#D32F2F" },
      warning: { main: "#ED6C02" },
    },

    // --------------------------------------------------------
    // 4) TIPOGRAFÍA CORPORATIVA
    // --------------------------------------------------------
    typography: {
      fontFamily: "Roboto, sans-serif",

      h1: { fontWeight: 700 },
      h2: { fontWeight: 700 },
      h3: { fontWeight: 700 },
      h4: { fontWeight: 600 },
      h5: { fontWeight: 600 },
      h6: { fontWeight: 500 },

      body1: { fontSize: "1rem" },
      body2: { fontSize: "0.9rem" },
    },

    // --------------------------------------------------------
    // 5) OVERRIDES DE COMPONENTES MUI
    // --------------------------------------------------------
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 6,
            textTransform: "none",
            fontWeight: 600,
            paddingLeft: 16,
            paddingRight: 16,
          },
        },
      },

      MuiPaper: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            transition: "background-color 0.3s ease",
          },
        },
      },

      MuiAppBar: {
        styleOverrides: {
          root: {
            backgroundColor: mode === "light" ? "#FFFFFF" : "#0F0F0F",
            color: mode === "light" ? colors.azul : colors.blanco,
            borderBottom: "1px solid rgba(0,0,0,0.1)",
          },
        },
      },
    },
  });
