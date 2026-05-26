import { Box, Typography, Paper, Stack, useTheme } from "@mui/material";

const AdminDashboard = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  return (
    <Box sx={{ p: 3 }}>
      {/* TÍTULO PRINCIPAL */}
      <Typography
        variant="h5"
        sx={{
          fontWeight: 700,
          mb: 3,
          color: isDark ? "#84CFED" : "#005CA2",
        }}
      >
        Panel de Administración
      </Typography>

      {/* CONTENEDOR PRINCIPAL */}
      <Paper
        elevation={3}
        sx={{
          p: 3,
          borderRadius: 3,
          background: isDark
            ? "rgba(42, 49, 57, 0.35)"
            : "rgba(255, 255, 255, 0.55)",
          backdropFilter: "blur(10px)",
          WebkitBackdropFilter: "blur(10px)",
          border: isDark ? "1px solid rgba(255,255,255,0.12)" : "none",
        }}
      >
        <Stack spacing={2}>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 600,
              color: isDark ? "#84CFED" : "#005CA2",
            }}
          >
            Bienvenido al Panel Administrativo
          </Typography>

          <Typography
            sx={{
              opacity: 0.9,
              color: isDark ? "#D0E8F2" : "#003B70",
              fontWeight: 500,
            }}
          >
            Desde aquí podrás gestionar agentes, parámetros y otras funciones
            administrativas del sistema.
          </Typography>
        </Stack>
      </Paper>
    </Box>
  );
};

export default AdminDashboard;
