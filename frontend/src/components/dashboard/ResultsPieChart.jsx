// ============================================================
//  RESULTS PIE CHART - DISTRIBUCIÓN DE RESULTADOS
// ============================================================
//
// Gráfico institucional tipo "torta" para mostrar:
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
// - data: [{ name: string, value: number }]
//
// ============================================================

import { Paper, Typography, Box, useTheme } from "@mui/material";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function ResultsPieChart({ data = [] }) {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  // Colores institucionales para OK / FAIL / WARNING
  const COLORS = ["#2ecc71", "#e74c3c", "#f1c40f"];

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
    data.every((d) => d.value === 0);

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
        Distribución de Resultados
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
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              outerRadius={100}
              dataKey="value"
              label
            >
              {data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
