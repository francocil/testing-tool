// ============================================================
// StepDetail.jsx (CON DOCUMENTOS + ASSERTS DEL PASO)
// Vista institucional del detalle de un paso
// ============================================================

import { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Divider,
  Button,
  Stack,
  Link,
} from "@mui/material";

import { useNavigate, useParams, Link as RouterLink } from "react-router-dom";
import axios from "../../api/axiosClient";

import DocumentList from "../../components/documents/DocumentList";
import DocumentUploader from "../../components/documents/DocumentUploader";

import {
  getDocumentosByPaso,
  uploadPasoDocumento,
  deletePasoDocumento,
  downloadPasoDocumento,
} from "../../api/pasoDocumentos";

import { usePermission } from "../../context/PermissionContext";

export default function StepDetail() {
  const { id, moduloId, casoId, pasoId } = useParams();
  const navigate = useNavigate();

  const [paso, setPaso] = useState(null);
  const [api, setApi] = useState(null);
  const [documentos, setDocumentos] = useState([]);
  const [asserts, setAsserts] = useState([]);
  const [loading, setLoading] = useState(true);

  const canViewDocs = usePermission("ver_documentos");
  const canCreateDocs = usePermission("crear_documentos");
  const canDeleteDocs = usePermission("eliminar_documentos");

  // -----------------------------
  // Cargar datos del paso
  // -----------------------------
  useEffect(() => {
    const loadPaso = async () => {
      try {
        const resPaso = await axios.get(`/pasos/${pasoId}`);
        setPaso(resPaso.data);

        // API asociada (si existe)
        if (resPaso.data.api_id) {
          const resApi = await axios.get(`/apis/${resPaso.data.api_id}`);
          setApi(resApi.data);
        }
      } catch (err) {
        console.error("Error cargando StepDetail", err);
      }

      setLoading(false);
    };

    loadPaso();
  }, [pasoId]);

  // -----------------------------
  // Cargar asserts del paso
  // -----------------------------
  useEffect(() => {
    const loadAsserts = async () => {
      try {
        const res = await axios.get(`/paso-assert/by-paso/${pasoId}`);
        setAsserts(res.data);
      } catch (err) {
        console.error("Error cargando asserts del paso", err);
      }
    };

    loadAsserts();
  }, [pasoId]);

  // -----------------------------
  // Cargar documentos del paso
  // -----------------------------
  const loadDocumentos = async () => {
    try {
      const data = await getDocumentosByPaso(pasoId);
      setDocumentos(data);
    } catch (err) {
      console.error("Error cargando documentos del paso", err);
    }
  };

  useEffect(() => {
    if (canViewDocs) loadDocumentos();
  }, [pasoId, canViewDocs]);

  // -----------------------------
  // Subir documento
  // -----------------------------
  const handleUpload = async (pasoId, file) => {
    await uploadPasoDocumento(pasoId, file);
    await loadDocumentos();
  };

  // -----------------------------
  // Eliminar documento
  // -----------------------------
  const handleDelete = async (id) => {
    await deletePasoDocumento(id);
    await loadDocumentos();
  };

  // -----------------------------
  // Descargar documento
  // -----------------------------
  const handleDownload = async (id, filename) => {
    await downloadPasoDocumento(id, filename);
  };

  if (loading) return <Typography>Cargando...</Typography>;
  if (!paso) return <Typography>No se encontró el paso.</Typography>;

  return (
    <Box p={3}>
      {/* ============================================================
        BREADCRUMB
      ============================================================ */}
      <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 2 }}>
        <Link component={RouterLink} to="/proyectos" underline="hover" color="primary">
          Proyectos
        </Link>

        <Typography>/</Typography>

        <Link
          component={RouterLink}
          to={`/proyectos/${id}`}
          underline="hover"
          color="primary"
        >
          Proyecto
        </Link>

        <Typography>/</Typography>

        <Link
          component={RouterLink}
          to={`/proyectos/${id}/modulos/${moduloId}`}
          underline="hover"
          color="primary"
        >
          Módulo
        </Link>

        <Typography>/</Typography>

        <Link
          component={RouterLink}
          to={`/proyectos/${id}/modulos/${moduloId}/casos/${casoId}`}
          underline="hover"
          color="primary"
        >
          Caso
        </Link>

        <Typography>/</Typography>

        <Typography fontWeight={700}>Paso {paso.orden}</Typography>
      </Stack>
      {/* ============================================================
        INFORMACIÓN DEL PASO
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Información del Paso</Typography>
        <Divider sx={{ my: 1 }} />

        <Typography><strong>ID:</strong> {paso.id}</Typography>
        <Typography><strong>Orden:</strong> {paso.orden}</Typography>
        <Typography><strong>Descripción:</strong> {paso.descripcion}</Typography>
        <Typography><strong>Fecha creación:</strong> {paso.fecha_creacion}</Typography>
      </Paper>

      {/* ============================================================
        API ASOCIADA
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">API Asociada</Typography>
        <Divider sx={{ my: 1 }} />

        {!api ? (
          <Typography>Este paso no tiene una API asociada.</Typography>
        ) : (
          <>
            <Typography><strong>Nombre:</strong> {api.nombre}</Typography>
            <Typography><strong>Método:</strong> {api.metodo}</Typography>
            <Typography><strong>Endpoint:</strong> {api.endpoint}</Typography>
            <Typography><strong>Base URL:</strong> {api.base_url}</Typography>
            <Typography><strong>Versión:</strong> {api.version}</Typography>

            <Button
              sx={{ mt: 1 }}
              variant="outlined"
              onClick={() => navigate(`/apis/${api.id}`)}
            >
              Ver API Completa
            </Button>
          </>
        )}
      </Paper>

      {/* ============================================================
        DOCUMENTOS DEL PASO
      ============================================================ */}
      {canViewDocs && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6">Documentos del Paso</Typography>
          <Divider sx={{ my: 1 }} />

          {canCreateDocs && (
            <Box sx={{ mb: 2 }}>
              <DocumentUploader pasoId={pasoId} onUpload={handleUpload} />
            </Box>
          )}

          <DocumentList
            documents={documentos}
            onDownload={handleDownload}
            onDelete={canDeleteDocs ? handleDelete : undefined}
          />
        </Paper>
      )}

      {/* ============================================================
        PARÁMETROS DEL PASO
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Parámetros del Paso</Typography>
        <Divider sx={{ my: 1 }} />

        {(!paso.parametros || paso.parametros.length === 0) ? (
          <Typography>No hay parámetros asociados.</Typography>
        ) : (
          (paso.parametros || []).map((p) => (
            <Paper key={p.id} sx={{ p: 1, mb: 1 }}>
              <Typography><strong>{p.nombre}</strong></Typography>
              <Typography>Tipo: {p.tipo}</Typography>
              <Typography>Valor por defecto: {p.valor_por_defecto || "—"}</Typography>
            </Paper>
          ))
        )}
      </Paper>

      {/* ============================================================
        ASSERTS DEL PASO
      ============================================================ */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6">Asserts del Paso</Typography>
        <Divider sx={{ my: 1 }} />

        {asserts.length === 0 ? (
          <Typography>No hay asserts definidos para este paso.</Typography>
        ) : (
          asserts.map((a) => (
            <Paper key={a.id} sx={{ p: 1, mb: 1 }}>
              <Typography><strong>Tipo:</strong> {a.tipo}</Typography>
              <Typography><strong>Expresión:</strong> {a.expresion}</Typography>
              <Typography><strong>Operador:</strong> {a.operador}</Typography>
              <Typography><strong>Valor esperado:</strong> {a.valor_esperado}</Typography>
              <Typography><strong>Mensaje error:</strong> {a.mensaje_error}</Typography>
              <Typography><strong>Orden:</strong> {a.orden}</Typography>
            </Paper>
          ))
        )}
      </Paper>
    </Box>
  );
}
