// ============================================================
//  QUICK ACTION CARD - ACCIONES RÁPIDAS (MODO CLARO/OSCURO)
// ============================================================
//
// Tarjeta institucional para accesos rápidos:
//
// ✔ Crear Proyecto
// ✔ Crear Caso de Prueba
// ✔ Crear Ejecución
// ✔ Ver Proyectos / Casos / Ejecuciones
//
// Características:
//
// - Estética institucional coherente con KpiCard y StatusCard
// - Soporte completo para modo claro/oscuro
// - Glassmorphism + animación suave
// - Íconos MUI
// - Navegación integrada con react-router
// - Componente reutilizable
//
// Props:
// - title: string
// - icon: JSX.Element
// - to: string (ruta de navegación)
// - color: string (color institucional base)
// ============================================================

import { Paper, Box, Typography, useTheme } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function QuickActionCard({ title, icon, to, color = "#005CA2" }) {
  const theme = useTheme();
  const navigate = useNavigate();
  const isDark = theme.palette.mode === "dark";

  // ============================================================
  //  ESTILOS DINÁMICOS SEGÚN MODO
  // ============================================================
  const background = isDark
    ? "rgba(42, 49, 57, 0.35)" // glass oscuro institucional
    : "rgba(255, 255, 255, 0.55)"; // glass claro institucional

  const textColor = isDark ? "#D0E8F2" : "#003B70";

  const iconBg = isDark
    ? "rgba(54, 83, 116, 0.43)" // azul institucional apagado
    : `${color}22`;

  const iconColor = isDark ? "#84CFED" : color;

  // ============================================================
  //  RENDER
  // ============================================================
  return (
    <Paper
      elevation={3}
      onClick={() => navigate(to)}
      sx={{
        p: 2.5,
        display: "flex",
        alignItems: "center",
        gap: 2,
        borderRadius: 3,
        background,
        backdropFilter: "blur(10px)",
        WebkitBackdropFilter: "blur(10px)",
        transition: "transform 0.25s ease, box-shadow 0.25s ease",
        cursor: "pointer",
        border: isDark ? "1px solid rgba(255,255,255,0.12)" : "none",

        "&:hover": {
          transform: "translateY(-3px)",
          boxShadow: isDark
            ? "0 6px 20px rgba(0,0,0,0.4)"
            : "0 6px 20px rgba(0,0,0,0.15)",
        },
      }}
    >
      {/* Ícono */}
      <Box
        sx={{
          width: 48,
          height: 48,
          borderRadius: "12px",
          backgroundColor: iconBg,
          color: iconColor,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 28,
        }}
      >
        {icon}
      </Box>

      {/* Texto */}
      <Box>
        <Typography
          variant="subtitle1"
          sx={{
            fontWeight: 600,
            color: textColor,
            opacity: 0.95,
          }}
        >
          {title}
        </Typography>
      </Box>
    </Paper>
  );
}
