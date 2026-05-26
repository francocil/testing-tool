// ============================================================
//  DETALLE DE MÓDULO (CON DOCUMENTOS INTEGRADOS)
// ============================================================
//
// - Muestra datos del módulo
// - Sección institucional de DOCUMENTOS DEL MÓDULO (NUEVO)
// - Integra listado de casos de prueba
// - Botón institucional “Nuevo Caso de Prueba”
// - Navegación Proyecto → Módulo → Caso
//
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Paper,
  Stack,
  Button,
} from "@mui/material";

import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";

// API módulo
import { getModulo } from "../../api/modulos";

// 👉 NUEVAS APIS DOCUMENTOS
import {
  getModuloDocumentos,
  uploadModuloDocumento,
  deleteModuloDocumento,
  downloadModuloDocumento,
} from "../../api/moduloDocumentos";

// 👉 NUEVOS COMPONENTES DOCUMENTOS
import DocumentUploader from "../../components/documents/DocumentUploader";
import DocumentList from "../../components/documents/DocumentList";

// Casos del módulo
import CaseList from "../casos/CaseList";

const ModuleDetail = () => {
  const { id, moduloId } = useParams();
  const navigate = useNavigate();

  const [modulo, setModulo] = useState(null);
  const [documentos, setDocumentos] = useState([]);

  // ------------------------------------------------------------
  // Cargar datos del módulo
  // ------------------------------------------------------------
  const loadModulo = async () => {
    const data = await getModulo(moduloId);
    setModulo(data);
  };

  // ------------------------------------------------------------
  // Cargar documentos del módulo
  // ------------------------------------------------------------
  const loadDocumentos = async () => {
    try {
      const data = await getModuloDocumentos();
      // Filtrar solo los documentos de este módulo
      setDocumentos(data.filter((d) => d.modulo_id === Number(moduloId)));
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadModulo();
    loadDocumentos();
  }, [moduloId]);

  const handleBack = () => navigate(`/proyectos/${id}`);
  const handleEdit = () =>
    navigate(`/proyectos/${id}/modulos/${moduloId}/editar`);

  const handleCreateCase = () =>
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos/crear`);

  if (!modulo) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Cargando módulo...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>

      {/* -------------------------------------------------------- */}
      {/* ENCABEZADO */}
      {/* -------------------------------------------------------- */}
      <Stack
        direction="row"
        spacing={2}
        alignItems="center"
        sx={{ mb: 3, justifyContent: "space-between" }}
      >
        <Stack direction="row" spacing={2} alignItems="center">
          <Button variant="text" startIcon={<ArrowBackIcon />} onClick={handleBack}>
            Volver
          </Button>

          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            Detalle del Módulo
          </Typography>
        </Stack>

        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={handleEdit}
          >
            Editar
          </Button>

          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateCase}
          >
            Nuevo Caso
          </Button>
        </Stack>
      </Stack>

      {/* -------------------------------------------------------- */}
      {/* TARJETA PRINCIPAL DEL MÓDULO */}
      {/* -------------------------------------------------------- */}
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
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          {modulo.nombre}
        </Typography>

        <Stack spacing={1} sx={{ mt: 2 }}>
          <Typography><strong>Tipo interfaz:</strong> {modulo.tipo_interfaz}</Typography>
          <Typography><strong>Tipo GUI:</strong> {modulo.tipo_gui}</Typography>
          <Typography><strong>Descripción:</strong> {modulo.descripcion || "Sin descripción"}</Typography>
          <Typography><strong>Fecha creación:</strong> {new Date(modulo.fecha_creacion).toLocaleString()}</Typography>
        </Stack>
      </Paper>

      {/* ============================================================ */}
      {/*  SECCIÓN INSTITUCIONAL: DOCUMENTOS DEL MÓDULO (NUEVO)       */}
      {/* ============================================================ */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Documentos del Módulo
        </Typography>

        {/* Subir documento */}
        <DocumentUploader
          label="Subir documento"
          pasoId={modulo.id}
          onUpload={async (moduloId, file) => {
            await uploadModuloDocumento(moduloId, file);
            loadDocumentos();
          }}
        />

        {/* Listado de documentos */}
        <Box sx={{ mt: 2 }}>
          <DocumentList
            documents={documentos}
            onDownload={(id, filename) => downloadModuloDocumento(id, filename)}
            onDelete={async (id) => {
              await deleteModuloDocumento(id);
              loadDocumentos();
            }}
          />
        </Box>
      </Box>

      {/* -------------------------------------------------------- */}
      {/* CASOS DE PRUEBA DEL MÓDULO */}
      {/* -------------------------------------------------------- */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Casos de Prueba del Módulo
        </Typography>

        <CaseList 
          proyectoId={id}
          moduloId={moduloId}
        />
      </Box>
    </Box>
  );
};

export default ModuleDetail;
