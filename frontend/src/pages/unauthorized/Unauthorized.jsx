import { Box, Typography } from "@mui/material";

export default function Unauthorized() {
  return (
    <div style={{ padding: 40, textAlign: "center" }}>
      <h1 style={{ color: "red" }}>Acceso denegado</h1>
      <p>No tenés permisos para acceder a esta sección.</p>
    </div>
  );
}

