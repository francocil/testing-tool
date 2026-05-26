// ============================================================
// DETALLE DE CASO DE PRUEBA + PASOS + DOCUMENTOS (CORREGIDO)
// + BOTÓN "EJECUTAR CASO" (UBICACIÓN A: ENCABEZADO)
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams, Link as RouterLink } from "react-router-dom";

import {
  Box,
  Paper,
  Stack,
  Typography,
  Button,
  Chip,
  Link,
} from "@mui/material";

import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

import { getCasoPrueba } from "../../api/casosPrueba";
import { getModulo } from "../../api/modulos";
import { getProyecto } from "../../api/proyectos";

import {
  getPasosByCaso,
  createPaso,
  updatePaso,
  deletePaso,
} from "../../api/pasos";

import {
  getDocumentosByPaso,
  uploadPasoDocumento,
  deletePasoDocumento,
  downloadPasoDocumento,
} from "../../api/pasoDocumentos";

import StepList from "../../components/steps/StepList";
import StepForm from "../../components/steps/StepForm";

const CaseDetail = () => {
  const { id, moduloId, casoId } = useParams();
  const navigate = useNavigate();

  const [caso, setCaso] = useState(null);
  const [modulo, setModulo] = useState(null);
  const [proyecto, setProyecto] = useState(null);

  const [pasos, setPasos] = useState([]);
  const [documentosPaso, setDocumentosPaso] = useState([]);

  const [openForm, setOpenForm] = useState(false);
  const [editData, setEditData] = useState(null);

  // ------------------------------------------------------------
  // Cargar caso
  // ------------------------------------------------------------
  const loadCaso = async () => {
    const data = await getCasoPrueba(casoId);
    setCaso(data);
  };

  // ------------------------------------------------------------
  // Cargar módulo y proyecto
  // ------------------------------------------------------------
  const loadModuloYProyecto = async () => {
    const m = await getModulo(moduloId);
    setModulo(m);

    const p = await getProyecto(m.proyecto_id);
    setProyecto(p);
  };

  // ------------------------------------------------------------
  // Cargar pasos del caso
  // ------------------------------------------------------------
  const loadPasos = async () => {
    const data = await getPasosByCaso(casoId);
    setPasos(data.sort((a, b) => a.orden - b.orden));
  };

  // ------------------------------------------------------------
  // Cargar documentos del paso
  // ------------------------------------------------------------
  const loadDocumentosPaso = async (pasoId) => {
    const data = await getDocumentosByPaso(pasoId);
    setDocumentosPaso(data);
  };

  useEffect(() => {
    loadCaso();
    loadModuloYProyecto();
    loadPasos();
  }, [casoId]);

  // ------------------------------------------------------------
  // Navegación
  // ------------------------------------------------------------
  const handleBack = () => {
    navigate(`/proyectos/${id}/modulos/${moduloId}`);
  };

  const handleEdit = () => {
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos/${casoId}/editar`);
  };

  // ⭐ CORREGIDO: usar caso.id REAL, no casoId del router
  const handleEjecutarCaso = () => {
    if (!caso) return;
    navigate(
      `/proyectos/${id}/modulos/${moduloId}/casos/${caso.id}/ejecucion`
    );
  };

  // ------------------------------------------------------------
  // Crear paso
  // ------------------------------------------------------------
  const handleCreatePaso = async (form) => {
    await createPaso({
      ...form,
      caso_id: Number(casoId),
    });

    setOpenForm(false);
    loadPasos();
  };

  // ------------------------------------------------------------
  // Editar paso
  // ------------------------------------------------------------
  const handleUpdatePaso = async (form) => {
    await updatePaso(editData.id, form);

    setOpenForm(false);
    setEditData(null);
    loadPasos();
  };

  // ------------------------------------------------------------
  // Eliminar paso
  // ------------------------------------------------------------
  const handleDeletePaso = async (idPaso) => {
    if (!window.confirm("¿Eliminar este paso?")) return;

    await deletePaso(idPaso);
    loadPasos();
  };

  // ------------------------------------------------------------
  // Ver detalle del paso
  // ------------------------------------------------------------
  const handleViewPaso = async (paso) => {
    navigate(
      `/proyectos/${id}/modulos/${moduloId}/casos/${caso.id}/pasos/${paso.id}`
    );
  };

  // ------------------------------------------------------------
  // Subir documento del paso
  // ------------------------------------------------------------
  const handleUploadDocumento = async (pasoId, file) => {
    await uploadPasoDocumento(pasoId, file);
    await loadDocumentosPaso(pasoId);
  };

  // ------------------------------------------------------------
  // Eliminar documento del paso
  // ------------------------------------------------------------
  const handleDeleteDocumento = async (idDoc, pasoId) => {
    await deletePasoDocumento(idDoc);
    await loadDocumentosPaso(pasoId);
  };
  // ------------------------------------------------------------
  // Render principal
  // ------------------------------------------------------------
  if (!caso) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Cargando caso de prueba...</Typography>
      </Box>
    );
  }

  return (
    <>
      <Box sx={{ p: 3 }}>
        {/* ============================================================
          BREADCRUMB
        ============================================================ */}
        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 2 }}>
          <Link component={RouterLink} to="/proyectos" underline="hover" color="primary">
            Proyectos
          </Link>

          <Typography>/</Typography>

          {proyecto && (
            <Link
              component={RouterLink}
              to={`/proyectos/${proyecto.id}`}
              underline="hover"
              color="primary"
            >
              {proyecto.nombre}
            </Link>
          )}

          <Typography>/</Typography>

          {modulo && (
            <Link
              component={RouterLink}
              to={`/proyectos/${proyecto?.id}/modulos/${modulo.id}`}
              underline="hover"
              color="primary"
            >
              {modulo.nombre}
            </Link>
          )}

          <Typography>/</Typography>

          <Typography fontWeight={700}>{caso.nombre}</Typography>
        </Stack>

        {/* ============================================================
          ENCABEZADO + BOTÓN EJECUTAR CASO
        ============================================================ */}
        <Stack
          direction="row"
          spacing={2}
          alignItems="center"
          sx={{ mb: 3, justifyContent: "space-between" }}
        >
          <Stack direction="row" spacing={2} alignItems="center">
            <Button variant="text" startIcon={<ArrowBackIcon />} onClick={handleBack}>
              Volver al Módulo
            </Button>

            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              Detalle del Caso de Prueba
            </Typography>
          </Stack>

          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              color="success"
              startIcon={<PlayArrowIcon />}
              onClick={handleEjecutarCaso}
            >
              Ejecutar Caso
            </Button>

            <Button variant="contained" startIcon={<EditIcon />} onClick={handleEdit}>
              Editar
            </Button>
          </Stack>
        </Stack>

        {/* ============================================================
          TARJETA PRINCIPAL DEL CASO (ACTUALIZADA)
        ============================================================ */}
        <Paper
          elevation={3}
          sx={{
            p: 3,
            borderRadius: 3,
            mb: 3,
            background: (theme) =>
              theme.palette.mode === "light"
                ? "rgba(255,255,255,0.85)"
                : "rgba(15,15,15,0.9)",
            backdropFilter: "blur(10px)",
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
            {caso.nombre}
          </Typography>

          <Typography variant="body1">
            <strong>Estado:</strong> {caso.estado || "—"}
          </Typography>

          <Typography variant="body1" sx={{ mt: 2 }}>
            <strong>Objetivo:</strong> {caso.objetivo || "—"}
          </Typography>

          <Typography variant="body1" sx={{ mt: 1 }}>
            <strong>Descripción:</strong> {caso.descripcion || "—"}
          </Typography>

          <Typography variant="body1" sx={{ mt: 1 }}>
            <strong>Precondiciones:</strong> {caso.precondiciones || "—"}
          </Typography>

          <Typography variant="body1" sx={{ mt: 1 }}>
            <strong>Postcondiciones:</strong> {caso.postcondiciones || "—"}
          </Typography>

          <Typography variant="body1" sx={{ mt: 1 }}>
            <strong>Porcentaje de aceptación:</strong>{" "}
            {caso.porcentaje_aceptacion != null
              ? `${caso.porcentaje_aceptacion}%`
              : "—"}
          </Typography>

          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
              Versión actual
            </Typography>

            <Chip
              label={`Versión ${caso.version_actual}`}
              color="primary"
              size="small"
            />
          </Box>
        </Paper>

        {/* ============================================================
          PASOS DEL CASO
        ============================================================ */}
        <Stack direction="row" justifyContent="flex-end" sx={{ mb: 1 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setEditData(null);
              setOpenForm(true);
            }}
          >
            Nuevo Paso
          </Button>
        </Stack>

        <StepList
          pasos={pasos}
          onView={handleViewPaso}
          onEdit={(paso) => {
            setEditData(paso);
            setOpenForm(true);
          }}
          onDelete={handleDeletePaso}
        />

        {/* MODAL FORM */}
        <StepForm
          open={openForm}
          onClose={() => {
            setOpenForm(false);
            setEditData(null);
          }}
          onSubmit={editData ? handleUpdatePaso : handleCreatePaso}
          initialData={editData}
        />
      </Box>
    </>
  );
};

export default CaseDetail;
