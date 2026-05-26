// ============================================================
//  RESULTS BAR CHART - COMPARATIVA DE RESULTADOS
// ============================================================
//
// Gráfico institucional tipo "barras" para mostrar:
//
// - OK
// - FAIL
// - WARNING
//
// Características:
//
// ✔ Glassmorphism institucional (claro/oscuro)
// ✔ Colores institucionales
// ✔ Recharts (ResponsiveContainer)
// ✔ Animación suave
// ✔ Manejo seguro cuando data está vacía
//
// Props:
// - data: [{ name: string, cantidad: number }]
//
// ============================================================

import { Paper, Typography, Box, useTheme } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function ResultsBarChart({ data = [] }) {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const background = isDark
    ? "rgba(42, 49, 57, 0.35)"
    : "rgba(255, 255, 255, 0.55)";

  const titleColor = isDark ? "#84CFED" : "#005CA2";

  // ============================================================
  //  MANEJO SEGURO DE DATA VACÍA
  // ============================================================
  const isEmpty =
    !Array.isArray(data) ||
    data.length === 0 ||
    data.every((d) => d.cantidad === 0);

  return (
    <Paper
      sx={{
        p: 3,
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
      <Typography
        variant="h6"
        sx={{
          mb: 2,
          fontWeight: 600,
          color: titleColor,
        }}
      >
        Comparativa de Resultados
      </Typography>

      {/* ============================================================ */}
      {/*  ESTADO VACÍO INSTITUCIONAL */}
      {/* ============================================================ */}
      {isEmpty ? (
        <Box
          sx={{
            textAlign: "center",
            opacity: 0.8,
            color: titleColor,
            py: 6,
          }}
        >
          <Typography variant="body1" sx={{ fontWeight: 600 }}>
            No hay datos suficientes para mostrar el gráfico
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Cuando existan ejecuciones registradas, aparecerán aquí.
          </Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="cantidad" fill="#005CA2" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
