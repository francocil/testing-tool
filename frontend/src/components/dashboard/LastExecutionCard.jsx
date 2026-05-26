// ============================================================
//  LAST EXECUTION CARD - TARJETA DE ÚLTIMA EJECUCIÓN
// ============================================================
//
// Componente institucional utilizado en el Dashboard para mostrar
// las últimas ejecuciones registradas.
//
// Características:
//
// ✔ Glassmorphism institucional (claro/oscuro)
// ✔ Ícono según estado (OK / FAIL / WARNING / PENDIENTE)
// ✔ Animación suave al hover
// ✔ Colores institucionales adaptados
// ✔ Protección ante valores undefined/null
//
// Props:
// - casoId: number
// - resultado: string ("OK" | "FAIL" | "WARNING" | null)
// - fecha: string (ISO) | null
// ============================================================

import { Paper, Box, Typography, useTheme } from "@mui/material";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import WarningIcon from "@mui/icons-material/Warning";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";

export default function LastExecutionCard({ casoId, resultado, fecha }) {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  // ============================================================
  //  ÍCONO SEGÚN ESTADO
  // ============================================================
  const getIcon = () => {
    switch (resultado) {
      case "OK":
        return <CheckCircleIcon />;
      case "FAIL":
        return <ErrorIcon />;
      case "WARNING":
        return <WarningIcon />;
      default:
        return <HourglassEmptyIcon />;
    }
  };

  // ============================================================
  //  COLOR SEGÚN ESTADO
  // ============================================================
  const getColor = () => {
    switch (resultado) {
      case "OK":
        return "#2ecc71";
      case "FAIL":
        return "#e74c3c";
      case "WARNING":
        return "#f1c40f";
      default:
        return "#3498db";
    }
  };

  const color = getColor();

  // ============================================================
  //  ESTILOS DINÁMICOS
  // ============================================================
  const background = isDark
    ? "rgba(42, 49, 57, 0.35)"
    : "rgba(255, 255, 255, 0.55)";

  const textColor = isDark ? "#D0E8F2" : "#003B70";

  const iconBg = isDark
    ? "rgba(54, 83, 116, 0.43)"
    : `${color}22`;

  const iconColor = isDark ? "#84CFED" : color;

  // ============================================================
  //  FECHA SEGURA
  // ============================================================
  let fechaFormateada = "—";
  try {
    fechaFormateada = fecha ? new Date(fecha).toLocaleString() : "—";
  } catch {
    fechaFormateada = "—";
  }

  // ============================================================
  //  RENDER
  // ============================================================
  return (
    <Paper
      elevation={3}
      sx={{
        p: 2.5,
        borderRadius: 3,
        background,
        backdropFilter: "blur(10px)",
        WebkitBackdropFilter: "blur(10px)",
        border: isDark ? "1px solid rgba(255,255,255,0.12)" : "none",
        transition: "transform 0.25s ease, box-shadow 0.25s ease",

        "&:hover": {
          transform: "translateY(-3px)",
          boxShadow: isDark
            ? "0 6px 20px rgba(0,0,0,0.4)"
            : "0 6px 20px rgba(0,0,0,0.15)",
        },
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        
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
          {getIcon()}
        </Box>

        {/* Texto */}
        <Box>
          <Typography
            variant="subtitle1"
            sx={{ fontWeight: 600, color: textColor }}
          >
            Caso #{casoId ?? "—"}
          </Typography>

          <Typography
            variant="body2"
            sx={{ opacity: 0.85, color: textColor }}
          >
            Estado: {resultado || "PENDIENTE"}
          </Typography>

          <Typography
            variant="caption"
            sx={{
              display: "block",
              mt: 1,
              opacity: 0.7,
              color: textColor,
            }}
          >
            Fecha: {fechaFormateada}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
}
