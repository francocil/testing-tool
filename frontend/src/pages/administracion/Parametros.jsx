import { Box, Typography, Paper } from "@mui/material";
import usePermission from "../../hooks/usePermission";

const Parametros = () => {
  // ============================================================
  // PERMISOS INSTITUCIONALES
  // ============================================================
  const { can } = usePermission();
  const puedeVer = can("seguridad_permiso_ver");

  // Si NO puede ver, no mostramos nada
  if (!puedeVer) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h6" color="error">
          No tenés permisos para ver parámetros del sistema.
        </Typography>
      </Box>
    );
  }

  // ============================================================
  // RENDER PRINCIPAL
  // ============================================================
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
        Gestión de Parámetros
      </Typography>

      <Paper
        elevation={3}
        sx={{
          p: 3,
          borderRadius: 3,
          background: (theme) =>
            theme.palette.mode === "light"
              ? "rgba(255,255,255,0.85)"
              : "rgba(15,15,15,0.9)",
          backdropFilter: "blur(10px)",
        }}
      >
        <Typography>
          Esta sección está destinada a la configuración de parámetros del
          sistema. Próximamente se integrarán las funcionalidades.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Parametros;
