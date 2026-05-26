// ============================================================
// CaseExecution.jsx (VERSIÓN CORREGIDA COMPLETA)
// ============================================================

import { useEffect, useMemo, useState } from "react";
import {
  Box,
  Paper,
  Stack,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TablePagination,
  Button,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import FlagIcon from "@mui/icons-material/Flag";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

import { useNavigate, useParams } from "react-router-dom";

import {
  crearEjecucion,
  getEjecucion,
  getEjecucionPasos,
  ejecutarEjecucion,
  ejecutarSiguientePaso,
} from "../../api/ejecuciones";

import { usePermission } from "../../context/PermissionContext";

// ============================================================
// Helpers
// ============================================================

const getEstadoColor = (estado) => {
  if (!estado) return "default";
  const e = estado.toLowerCase();
  if (e.includes("ok")) return "success";
  if (e.includes("error") || e.includes("fallo")) return "error";
  if (e.includes("simulado")) return "info";
  return "default";
};

const prettyJson = (value) => {
  if (!value) return "";
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
};

// ============================================================
// Componente principal
// ============================================================

const CaseExecution = () => {
  const navigate = useNavigate();
  const { id: proyectoId, moduloId, casoId } = useParams();

  const [ejecucion, setEjecucion] = useState(null);
  const [pasos, setPasos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [runningAuto, setRunningAuto] = useState(false);
  const [runningStep, setRunningStep] = useState(false);
  const [error, setError] = useState(null);

  const [selectedPaso, setSelectedPaso] = useState(null);

  // Paginación
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const ejecucionId = ejecucion?.id;

  const loadEjecucionAndPasos = async (id) => {
    try {
      setLoading(true);
      setError(null);
      const [ej, ps] = await Promise.all([
        getEjecucion(id),
        getEjecucionPasos(id),
      ]);
      setEjecucion(ej);
      setPasos(ps || []);
    } catch (err) {
      console.error(err);
      setError("No se pudo cargar la ejecución.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (ejecucionId) {
      loadEjecucionAndPasos(ejecucionId);
    }
  }, [ejecucionId]);

  // ==========================================================
  // Crear ejecución
  // ==========================================================
  const { user } = usePermission();

  const handleCrearEjecucion = async (modo = "automatico") => {
    try {
      setCreating(true);
      setError(null);

      const nueva = await crearEjecucion({
        caso_id: Number(casoId),
        usuario_id: user.id,
        modo,
      });

      setEjecucion(nueva);
      setPasos([]);
      setSelectedPaso(null);
    } catch (err) {
      console.error(err);
      setError("No se pudo crear la ejecución.");
    } finally {
      setCreating(false);
    }
  };

  // ==========================================================
  // Ejecutar caso completo (automático)
  // ==========================================================
  const handleEjecutarAutomatico = async () => {
    let id = ejecucionId;
    try {
      setRunningAuto(true);
      setError(null);

      if (!id) {
        const nueva = await crearEjecucion({
          caso_id: Number(casoId),
          usuario_id: user.id,
          modo: "automatico",
        });
        setEjecucion(nueva);
        id = nueva.id;
      }

      if (!id) return;

      const ej = await ejecutarEjecucion(id);
      setEjecucion(ej);

      const ps = await getEjecucionPasos(id);
      setPasos(ps || []);
    } catch (err) {
      console.error(err);
      setError("Error al ejecutar el caso completo.");
    } finally {
      setRunningAuto(false);
    }
  };

  // ==========================================================
  // Ejecutar siguiente paso (paso a paso)
  // ==========================================================
  const handleEjecutarSiguientePaso = async () => {
    let id = ejecucionId;
    try {
      setRunningStep(true);
      setError(null);

      if (!id) {
        const nueva = await crearEjecucion({
          caso_id: Number(casoId),
          usuario_id: user.id,
          modo: "paso_a_paso",
        });
        setEjecucion(nueva);
        id = nueva.id;
      }

      if (!id) return;

      const ej = await ejecutarSiguientePaso(id);
      setEjecucion(ej);

      const ps = await getEjecucionPasos(id);
      setPasos(ps || []);
    } catch (err) {
      console.error(err);
      setError("Error al ejecutar el siguiente paso.");
    } finally {
      setRunningStep(false);
    }
  };

  // ==========================================================
  // Datos derivados
  // ==========================================================
  const pasosOrdenados = useMemo(() => {
    return [...pasos].sort((a, b) => (a.orden ?? 0) - (b.orden ?? 0));
  }, [pasos]);

  const paginated = useMemo(() => {
    const start = page * rowsPerPage;
    return pasosOrdenados.slice(start, start + rowsPerPage);
  }, [pasosOrdenados, page, rowsPerPage]);

  const resumen = useMemo(() => {
    const total = pasos.length;
    const ok = pasos.filter((p) =>
      (p.tipo_resultado || "").toLowerCase().includes("ok")
    ).length;
    const errorCount = pasos.filter((p) =>
      (p.tipo_resultado || "").toLowerCase().includes("error")
    ).length;
    const porcentaje = total > 0 ? Math.round((ok * 100) / total) : 0;
    return { total, ok, error: errorCount, porcentaje };
  }, [pasos]);

  // ==========================================================
  // UI
  // ==========================================================
  const handleVolver = () => {
    navigate(
      `/proyectos/${proyectoId}/modulos/${moduloId}/casos/${casoId}`
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* ENCABEZADO */}
      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={handleVolver}
        >
          Volver al caso
        </Button>

        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Ejecución del Caso #{casoId}
        </Typography>

        {ejecucion && (
          <Chip
            label={ejecucion.estado || "SIN ESTADO"}
            color={getEstadoColor(ejecucion.estado)}
            sx={{ ml: 2 }}
          />
        )}
      </Stack>

      {/* RESUMEN + CONTROLES */}
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <Paper elevation={3} sx={{ p: 2, flex: 1, borderRadius: 3 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
            Resumen de ejecución
          </Typography>
          <Stack direction="row" spacing={3}>
            <Box>
              <Typography variant="body2" color="text.secondary">
                Total pasos
              </Typography>
              <Typography variant="h6">{resumen.total}</Typography>
            </Box>
            <Box>
              <Typography variant="body2" color="text.secondary">
                OK
              </Typography>
              <Typography variant="h6" color="success.main">
                {resumen.ok}
              </Typography>
            </Box>
            <Box>
              <Typography variant="body2" color="text.secondary">
                Error
              </Typography>
              <Typography variant="h6" color="error.main">
                {resumen.error}
              </Typography>
            </Box>
            <Box>
              <Typography variant="body2" color="text.secondary">
                Éxito
              </Typography>
              <Typography variant="h6">{resumen.porcentaje}%</Typography>
            </Box>
          </Stack>
        </Paper>

        <Paper elevation={3} sx={{ p: 2, minWidth: 320, borderRadius: 3 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
            Controles de ejecución
          </Typography>
          <Stack direction="row" spacing={1}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              startIcon={<PlayArrowIcon />}
              onClick={handleEjecutarAutomatico}
              disabled={creating || runningAuto || loading}
            >
              Ejecutar caso completo
            </Button>
            <Button
              fullWidth
              variant="outlined"
              color="primary"
              startIcon={<SkipNextIcon />}
              onClick={handleEjecutarSiguientePaso}
              disabled={creating || runningStep || loading}
            >
              Siguiente paso
            </Button>
          </Stack>
          {error && (
            <Typography variant="caption" color="error" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}
        </Paper>
      </Stack>

      {/* GRILLA DE PASOS */}
      <Paper elevation={3} sx={{ borderRadius: 3, overflow: "hidden", mb: 2 }}>
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Pasos ejecutados
          </Typography>
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell width={40}></TableCell>
              <TableCell>Orden</TableCell>
              <TableCell>Nombre del paso</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell>Resultado</TableCell>
              <TableCell>Fecha</TableCell>
              <TableCell align="right">Acciones</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {paginated.map((p) => (
              <TableRow
                key={p.id}
                hover
                sx={{ cursor: "pointer" }}
                onClick={() => setSelectedPaso(p)}
              >
                <TableCell>
                  <FlagIcon color="primary" />
                </TableCell>

                <TableCell>{p.orden ?? "-"}</TableCell>
                <TableCell>{p.nombre_paso ?? `Paso ${p.orden}`}</TableCell>

                <TableCell>
                  <Chip
                    label={p.tipo_resultado || "SIN ESTADO"}
                    color={getEstadoColor(p.tipo_resultado)}
                    size="small"
                  />
                </TableCell>

                <TableCell>{p.tipo_resultado || "-"}</TableCell>

                <TableCell>
                  {p.fecha ? new Date(p.fecha).toLocaleString() : "-"}
                </TableCell>

                <TableCell align="right">
                  <Button
                    size="small"
                    variant="contained"
                    color="primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedPaso(p);
                    }}
                  >
                    Ver detalle
                  </Button>
                </TableCell>
              </TableRow>
            ))}

            {paginated.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography variant="body2" color="text.secondary">
                    No hay pasos ejecutados aún. Ejecutá el caso o el siguiente
                    paso.
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>

        <TablePagination
          component="div"
          count={pasosOrdenados.length}
          page={page}
          onPageChange={(e, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          labelRowsPerPage="Filas por página"
        />
      </Paper>

      {/* DETALLE DEL PASO SELECCIONADO */}
      {selectedPaso && (
        <Paper
          elevation={3}
          sx={{
            borderRadius: 3,
            p: 2,
          }}
        >
          <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Detalle del paso ejecutado
            </Typography>

            <Button size="small" onClick={() => setSelectedPaso(null)}>
              Cerrar detalle
            </Button>
          </Stack>

          <Divider sx={{ mb: 2 }} />

          <Typography variant="subtitle1" sx={{ mb: 1 }}>
            {`Paso ${selectedPaso.orden ?? ""} — ${
              selectedPaso.nombre_paso ?? ""
            }`}
          </Typography>

          <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
            <Chip
              label={selectedPaso.tipo_resultado || "SIN ESTADO"}
              color={getEstadoColor(selectedPaso.tipo_resultado)}
            />
            {selectedPaso.duracion_ms && (
              <Chip
                label={`Duración: ${selectedPaso.duracion_ms.toFixed(1)} ms`}
                color="info"
              />
            )}
          </Stack>

          {/* REQUEST */}
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography sx={{ fontWeight: 600 }}>Request</Typography>
            </AccordionSummary>

            <AccordionDetails>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mb: 1 }}
              >
                Detalle del request enviado por el motor.
              </Typography>

              <pre
                style={{
                  margin: 0,
                  padding: "8px 12px",
                  background: "#111",
                  color: "#0f0",
                  borderRadius: 8,
                  maxHeight: 300,
                  overflow: "auto",
                  fontSize: 12,
                }}
              >
                {selectedPaso.request_json
                  ? prettyJson(selectedPaso.request_json)
                  : "// Sin datos de request"}
              </pre>
            </AccordionDetails>
          </Accordion>

          {/* RESPONSE */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography sx={{ fontWeight: 600 }}>Response</Typography>
            </AccordionSummary>

            <AccordionDetails>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mb: 1 }}
              >
                Detalle del response recibido.
              </Typography>

              <pre
                style={{
                  margin: 0,
                  padding: "8px 12px",
                  background: "#111",
                  color: "#0ff",
                  borderRadius: 8,
                  maxHeight: 300,
                  overflow: "auto",
                  fontSize: 12,
                }}
              >
                {selectedPaso.response_json
                  ? prettyJson(selectedPaso.response_json)
                  : "// Sin datos de response"}
              </pre>
            </AccordionDetails>
          </Accordion>

          {/* ASSERTS */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography sx={{ fontWeight: 600 }}>Asserts</Typography>
            </AccordionSummary>

            <AccordionDetails>
              {selectedPaso.asserts_json &&
              selectedPaso.asserts_json.length > 0 ? (
                selectedPaso.asserts_json.map((a, idx) => (
                  <Box key={idx} sx={{ mb: 2 }}>
                    <Typography
                      variant="subtitle2"
                      sx={{ fontWeight: 600, mb: 0.5 }}
                    >
                      Assert #{idx + 1}
                    </Typography>
                    <pre
                      style={{
                        margin: 0,
                        padding: "8px 12px",
                        background: "#222",
                        color: "#fff",
                        borderRadius: 8,
                        maxHeight: 200,
                        overflow: "auto",
                        fontSize: 12,
                      }}
                    >
                      {prettyJson(a)}
                    </pre>
                  </Box>
                ))
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No hay asserts registrados para este paso.
                </Typography>
              )}
            </AccordionDetails>
          </Accordion>

          {/* ERRORES */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography sx={{ fontWeight: 600 }}>Errores técnicos</Typography>
            </AccordionSummary>

            <AccordionDetails>
              {selectedPaso.errores_json &&
              selectedPaso.errores_json.length > 0 ? (
                selectedPaso.errores_json.map((err, idx) => (
                  <Typography key={idx} color="error" sx={{ mb: 1 }}>
                    {err}
                  </Typography>
                ))
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No se registraron errores técnicos.
                </Typography>
              )}
            </AccordionDetails>
          </Accordion>
        </Paper>
      )}
    </Box>
  );
};

export default CaseExecution;
