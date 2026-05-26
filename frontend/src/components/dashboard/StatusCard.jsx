// ============================================================
//  STATUS CARD - TARJETA DE ESTADO (MODO CLARO/OSCURO)
// ============================================================
//
// Componente institucional utilizado en el Dashboard para mostrar
// estados globales de ejecuciones:
//
// ✔ OK
// ✔ FAIL
// ✔ WARNING
// ✔ PENDIENTE
//
// Características:
//
// - Glassmorphism institucional (claro/oscuro)
// - Íconos MUI con fondo institucional
// - Animación suave al hover
// - Diseño consistente con KpiCard y QuickActionCard
// - Protección ante valores undefined/null
//
// Props:
// - title: string
// - value: string|number
// - icon: JSX.Element
// - color: string (color base del estado)
// ============================================================

import { Paper, Box, Typography, useTheme } from "@mui/material";

export default function StatusCard({ title, value, icon, color }) {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  // ============================================================
  //  ESTILOS DINÁMICOS SEGÚN MODO
  // ============================================================
  const background = isDark
    ? "rgba(42, 49, 57, 0.35)" // glass oscuro institucional
    : "rgba(255, 255, 255, 0.55)"; // glass claro institucional

  const textColor = isDark ? "#D0E8F2" : "#003B70";
  const valueColor = isDark ? "#84CFED" : color;

  const iconBg = isDark
    ? "rgba(54, 83, 116, 0.43)" // azul institucional apagado
    : `${color}22`;

  const iconColor = isDark ? "#84CFED" : color;

  // Protección ante valores undefined/null
  const safeValue = value ?? "—";

  // ============================================================
  //  RENDER
  // ============================================================
  return (
    <Paper
      elevation={3}
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
        cursor: "default",
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
          variant="subtitle2"
          sx={{
            fontWeight: 600,
            opacity: 0.9,
            color: textColor,
          }}
        >
          {title}
        </Typography>

        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
            color: valueColor,
            lineHeight: 1.2,
          }}
        >
          {safeValue}
        </Typography>
      </Box>
    </Paper>
  );
}
