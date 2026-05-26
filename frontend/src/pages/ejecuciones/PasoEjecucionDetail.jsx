// ============================================================
// PasoEjecucionDetail.jsx
// Vista institucional del resultado de un paso ejecutado
// ============================================================

import { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Divider,
  Stack,
  Chip,
} from "@mui/material";

import { useParams } from "react-router-dom";
import axios from "../../api/axiosClient";

export default function PasoEjecucionDetail() {
  const { ejecucionId, pasoId } = useParams();

  const [ejecPaso, setEjecPaso] = useState(null);
  const [paso, setPaso] = useState(null);
  const [requestInfo, setRequestInfo] = useState(null);
  const [responseInfo, setResponseInfo] = useState(null);
  const [asserts, setAsserts] = useState([]);
  const [loading, setLoading] = useState(true);

  // ------------------------------------------------------------
  // Cargar datos del paso ejecutado
  // ------------------------------------------------------------
  useEffect(() => {
    const loadData = async () => {
      try {
        // 1) Obtener EjecucionPaso
        const res = await axios.get(
          `/ejecuciones/${ejecucionId}/pasos/${pasoId}`
        );
        setEjecPaso(res.data);

        // 2) Obtener Paso original
        const resPaso = await axios.get(`/pasos/${pasoId}`);
        setPaso(resPaso.data);

        // 3) Parsear request/response
        if (res.data.valor_obtenido) {
          try {
            const parsed = JSON.parse(res.data.valor_obtenido);

            setRequestInfo(parsed.request || null);
            setResponseInfo(parsed.response || null);
          } catch {
            // valor_obtenido no es JSON válido
          }
        }

        // 4) Obtener asserts del paso
        const resAsserts = await axios.get(`/paso-assert/by-paso/${pasoId}`);
        setAsserts(resAsserts.data);
      } catch (err) {
        console.error("Error cargando ejecución del paso", err);
      }

      setLoading(false);
    };

    loadData();
  }, [ejecucionId, pasoId]);

  if (loading) return <Typography>Cargando...</Typography>;
  if (!ejecPaso) return <Typography>No se encontró la ejecución del paso.</Typography>;

  return (
    <Box p={3}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Resultado del Paso {paso?.orden}
      </Typography>

      {/* ============================================================
        INFORMACIÓN GENERAL
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Información General</Typography>
        <Divider sx={{ my: 1 }} />

        <Typography><strong>Resultado:</strong> {ejecPaso.resultado}</Typography>
        <Typography><strong>Fecha:</strong> {ejecPaso.fecha}</Typography>

        <Chip
          label={ejecPaso.resultado.toUpperCase()}
          color={ejecPaso.resultado === "ok" ? "success" : "error"}
          sx={{ mt: 1 }}
        />
      </Paper>
      {/* ============================================================
        REQUEST
      ============================================================ */}
      {requestInfo && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6">Request Enviado</Typography>
          <Divider sx={{ my: 1 }} />

          <Typography><strong>Método:</strong> {requestInfo.method}</Typography>
          <Typography><strong>URL:</strong> {requestInfo.url}</Typography>

          <Typography sx={{ mt: 1 }}><strong>Headers:</strong></Typography>
          <pre>{JSON.stringify(requestInfo.headers, null, 2)}</pre>

          <Typography sx={{ mt: 1 }}><strong>Query:</strong></Typography>
          <pre>{JSON.stringify(requestInfo.query, null, 2)}</pre>

          <Typography sx={{ mt: 1 }}><strong>Body:</strong></Typography>
          <pre>{JSON.stringify(requestInfo.payload, null, 2)}</pre>
        </Paper>
      )}

      {/* ============================================================
        RESPONSE
      ============================================================ */}
      {responseInfo && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6">Response Recibido</Typography>
          <Divider sx={{ my: 1 }} />

          <Typography><strong>Status:</strong> {responseInfo.status_code}</Typography>

          <Typography sx={{ mt: 1 }}><strong>Headers:</strong></Typography>
          <pre>{JSON.stringify(responseInfo.headers, null, 2)}</pre>

          <Typography sx={{ mt: 1 }}><strong>Body:</strong></Typography>
          <pre>{responseInfo.body}</pre>

          <Typography sx={{ mt: 1 }}><strong>JSON:</strong></Typography>
          <pre>{JSON.stringify(responseInfo.json, null, 2)}</pre>
        </Paper>
      )}

      {/* ============================================================
        ASSERTS EJECUTADOS
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Asserts Ejecutados</Typography>
        <Divider sx={{ my: 1 }} />

        {asserts.length === 0 ? (
          <Typography>No hay asserts definidos.</Typography>
        ) : (
          asserts.map((a) => {
            const fallo =
              ejecPaso.valor_obtenido &&
              ejecPaso.valor_obtenido.includes(a.mensaje_error);

            return (
              <Paper
                key={a.id}
                sx={{
                  p: 1,
                  mb: 1,
                  borderLeft: `4px solid ${
                    fallo ? "#d32f2f" : "#2e7d32"
                  }`,
                }}
              >
                <Typography><strong>{a.tipo}</strong> — {a.expresion}</Typography>
                <Typography>{a.operador} {a.valor_esperado}</Typography>

                <Chip
                  label={fallo ? "ERROR" : "OK"}
                  color={fallo ? "error" : "success"}
                  size="small"
                  sx={{ mt: 1 }}
                />

                {fallo && (
                  <Typography sx={{ mt: 1, color: "error.main" }}>
                    {a.mensaje_error}
                  </Typography>
                )}
              </Paper>
            );
          })
        )}
      </Paper>
    </Box>
  );
}
