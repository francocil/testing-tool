// ============================================================
// EjecucionDetail.jsx
// Vista institucional de la ejecución completa de un caso
// ============================================================

import { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Divider,
  Chip,
  Stack,
  Button,
} from "@mui/material";

import { useParams, useNavigate } from "react-router-dom";
import axios from "../../api/axiosClient";

export default function EjecucionDetail() {
  const { ejecucionId } = useParams();
  const navigate = useNavigate();

  const [ejecucion, setEjecucion] = useState(null);
  const [loading, setLoading] = useState(true);

  // ------------------------------------------------------------
  // Cargar ejecución completa
  // ------------------------------------------------------------
  useEffect(() => {
    const load = async () => {
      try {
        const res = await axios.get(`/ejecuciones/${ejecucionId}`);
        setEjecucion(res.data);
      } catch (err) {
        console.error("Error cargando ejecución", err);
      }
      setLoading(false);
    };

    load();
  }, [ejecucionId]);

  if (loading) return <Typography>Cargando...</Typography>;
  if (!ejecucion) return <Typography>No se encontró la ejecución.</Typography>;

  const pasos = ejecucion.pasos || [];
  const contexto = ejecucion.contexto || {};
  return (
    <Box p={3}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Ejecución #{ejecucion.id}
      </Typography>

      {/* ============================================================
        INFORMACIÓN GENERAL
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Información General</Typography>
        <Divider sx={{ my: 1 }} />

        <Typography><strong>Estado:</strong> {ejecucion.estado}</Typography>
        <Typography><strong>Modo:</strong> {ejecucion.modo}</Typography>
        <Typography><strong>Resultado global:</strong> {ejecucion.resultado_global}</Typography>
        <Typography><strong>Porcentaje aceptación:</strong> {ejecucion.porcentaje_aceptacion}%</Typography>
        <Typography><strong>Fecha inicio:</strong> {ejecucion.fecha}</Typography>
        <Typography><strong>Fecha fin:</strong> {ejecucion.fecha_fin || "—"}</Typography>

        <Chip
          label={ejecucion.resultado_global?.toUpperCase()}
          color={ejecucion.resultado_global === "ok" ? "success" : "error"}
          sx={{ mt: 1 }}
        />
      </Paper>

      {/* ============================================================
        TIMELINE DE PASOS
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Pasos Ejecutados</Typography>
        <Divider sx={{ my: 1 }} />

        {pasos.length === 0 ? (
          <Typography>No hay pasos ejecutados.</Typography>
        ) : (
          pasos
            .sort((a, b) => a.paso.orden - b.paso.orden)
            .map((ep) => (
              <Paper
                key={ep.id}
                sx={{
                  p: 2,
                  mb: 1,
                  borderLeft: `4px solid ${
                    ep.resultado === "ok" ? "#2e7d32" : ep.resultado === "error" ? "#d32f2f" : "#1976d2"
                  }`,
                }}
              >
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <div>
                    <Typography>
                      <strong>Paso {ep.paso.orden}:</strong> {ep.paso.nombre}
                    </Typography>
                    <Typography variant="body2">
                      Resultado: {ep.resultado}
                    </Typography>
                    <Typography variant="body2">
                      Fecha: {ep.fecha}
                    </Typography>
                  </div>

                  <Button
                    variant="outlined"
                    onClick={() =>
                      navigate(`/ejecuciones/${ejecucionId}/pasos/${ep.paso_id}`)
                    }
                  >
                    Ver Detalle
                  </Button>
                </Stack>
              </Paper>
            ))
        )}
      </Paper>

      {/* ============================================================
        CONTEXTO FINAL
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Contexto Final</Typography>
        <Divider sx={{ my: 1 }} />

        {Object.keys(contexto).length === 0 ? (
          <Typography>No se generaron variables de contexto.</Typography>
        ) : (
          <pre>{JSON.stringify(contexto, null, 2)}</pre>
        )}
      </Paper>
    </Box>
  );
}
