// ============================================================
//  DETALLE DE PROYECTO (CON DOCUMENTOS + INSTITUCIONAL + MÓDULOS)
// ============================================================
// - Muestra datos del proyecto
// - Sección institucional (Repartición, Dirección, Área)
// - Sección de DOCUMENTOS del proyecto
// - Sección de MÓDULOS del proyecto
// - Diseño institucional (glass, colores, tipografía)
// - Navegación limpia y trazabilidad completa
// - 🔥 Protección institucional por permisos
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Paper,
  Stack,
  Button,
  Divider,
} from "@mui/material";

import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import EditIcon from "@mui/icons-material/Edit";

// API proyecto
import { getProyecto } from "../../api/proyectos";

// APIS DOCUMENTOS
import {
  getProyectoDocumentos,
  uploadProyectoDocumento,
  deleteProyectoDocumento,
  downloadProyectoDocumento,
} from "../../api/proyectoDocumentos";

// COMPONENTES DOCUMENTOS
import DocumentUploader from "../../components/documents/DocumentUploader";
import DocumentList from "../../components/documents/DocumentList";

// LISTADO DE MÓDULOS
import ModuleList from "../modulos/ModuleList";

// 🔥 PERMISOS INSTITUCIONALES
import { usePermission } from "../../context/PermissionContext";

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { can } = usePermission(); // 🔥 permisos

  const [proyecto, setProyecto] = useState(null);
  const [documentos, setDocumentos] = useState([]);
  const [error, setError] = useState(null);

  // ============================================================
  // 1) PROTECCIÓN DE ACCESO
  // ============================================================
  if (!can("ver_proyectos")) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h4" color="error" fontWeight={700}>
          Acceso denegado
        </Typography>
        <Typography sx={{ mt: 1 }}>
          No tenés permiso para ver este proyecto.
        </Typography>
      </Box>
    );
  }

  // ------------------------------------
  // Cargar datos del proyecto
  // ------------------------------------
  const loadProyecto = async () => {
    try {
      const data = await getProyecto(id);
      setProyecto(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("No se pudo cargar el proyecto.");
    }
  };

  // ------------------------------------
  // Cargar documentos del proyecto
  // ------------------------------------
  const loadDocumentos = async () => {
    try {
      const data = await getProyectoDocumentos();
      setDocumentos(data.filter((d) => d.proyecto_id === Number(id)));
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadProyecto();
    loadDocumentos();
  }, [id]);

  const handleBack = () => navigate("/proyectos");

  const handleEdit = () => {
    if (!can("editar_proyectos")) {
      alert("No tenés permiso para editar proyectos.");
      return;
    }
    navigate(`/proyectos/${id}/editar`);
  };

  // ------------------------------------
  // ESTADOS: error / cargando
  // ------------------------------------
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!proyecto) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Cargando proyecto...</Typography>
      </Box>
    );
  }

  // Helpers institucionales
  const reparticionNombre = proyecto.reparticion?.nombre || "Sin repartición asignada";
  const direccionNombre = proyecto.direccion?.nombre || "Sin dirección asignada";
  const areaNombre = proyecto.area?.nombre || "Sin área asignada";

  // ====================================
  //  RENDER PRINCIPAL
  // ====================================
  return (
    <Box sx={{ p: 3 }}>

      {/* ------------------------------- */}
      {/* ENCABEZADO */}
      {/* ------------------------------- */}
      <Box
        sx={{
          mb: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Stack direction="row" spacing={2} alignItems="center">
          <Button variant="text" startIcon={<ArrowBackIcon />} onClick={handleBack}>
            Volver
          </Button>

          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            Detalle del Proyecto
          </Typography>
        </Stack>

        {/* 🔥 EDITAR PROTEGIDO */}
        {can("editar_proyectos") && (
          <Button variant="outlined" startIcon={<EditIcon />} onClick={handleEdit}>
            Editar
          </Button>
        )}
      </Box>

      {/* -------------------------------------- */}
      {/* TARJETA PRINCIPAL DEL PROYECTO */}
      {/* -------------------------------------- */}
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
        <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
          {proyecto.nombre}
        </Typography>

        <Stack spacing={1} sx={{ mt: 1 }}>
          <Typography variant="body2" color="text.secondary">
            ID: {proyecto.id}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Estado: {proyecto.estado} — Versión: {proyecto.version}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Fecha de creación:{" "}
            {proyecto.fecha_creacion
              ? new Date(proyecto.fecha_creacion).toLocaleString()
              : "-"}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Última actualización:{" "}
            {proyecto.fecha_actualizacion
              ? new Date(proyecto.fecha_actualizacion).toLocaleString()
              : "-"}
          </Typography>

          <Divider sx={{ my: 2 }} />

          {/* OBJETIVO */}
          <Box sx={{ mt: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Objetivo general
            </Typography>
            <Typography variant="body1">
              {proyecto.objetivo_general || "Sin objetivo definido."}
            </Typography>
          </Box>

          {/* CONTEXTO */}
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Contexto
            </Typography>
            <Typography variant="body1">
              {proyecto.contexto || "Sin contexto definido."}
            </Typography>
          </Box>
        </Stack>
      </Paper>

      {/* ============================================================ */}
      {/*  SECCIÓN INSTITUCIONAL: REPARTICIÓN / DIRECCIÓN / ÁREA      */}
      {/* ============================================================ */}
      <Paper
        elevation={2}
        sx={{
          p: 3,
          mb: 3,
          borderRadius: 3,
          background: (theme) =>
            theme.palette.mode === "light"
              ? "rgba(255,255,255,0.9)"
              : "rgba(20,20,20,0.95)",
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Información institucional
        </Typography>

        <Stack spacing={1}>
          <Typography variant="body2">
            <strong>Repartición:</strong> {reparticionNombre}
          </Typography>

          <Typography variant="body2">
            <strong>Dirección:</strong> {direccionNombre}
          </Typography>

          <Typography variant="body2">
            <strong>Área:</strong> {areaNombre}
          </Typography>
        </Stack>
      </Paper>

      {/* ====================================== */}
      {/*  SECCIÓN: DOCUMENTOS DEL PROYECTO      */}
      {/* ====================================== */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Documentos del Proyecto
        </Typography>

        {/* 🔥 SUBIR DOCUMENTO (solo si puede editar) */}
        {can("editar_proyectos") && (
          <DocumentUploader
            label="Subir documento"
            pasoId={proyecto.id}
            onUpload={async (proyectoId, file) => {
              await uploadProyectoDocumento(proyectoId, file);
              loadDocumentos();
            }}
          />
        )}

        {/* Listado de documentos */}
        <Box sx={{ mt: 2 }}>
          <DocumentList
            documents={documentos}
            onDownload={(docId, filename) =>
              downloadProyectoDocumento(docId, filename)
            }
            onDelete={
              can("editar_proyectos")
                ? async (docId) => {
                    await deleteProyectoDocumento(docId);
                    loadDocumentos();
                  }
                : null
            }
          />
        </Box>
      </Box>

      {/* ====================================== */}
      {/*  SECCIÓN: MÓDULOS DEL PROYECTO         */}
      {/* ====================================== */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Módulos del Proyecto
        </Typography>

        <ModuleList proyectoId={proyecto.id} />
      </Box>

      {/* -------------------------------------- */}
      {/* SECCIÓN FUTURA                         */}
      {/* -------------------------------------- */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mt: 4,
          borderRadius: 3,
          background: (theme) =>
            theme.palette.mode === "light"
              ? "rgba(255,255,255,0.7)"
              : "rgba(20,20,20,0.9)",
        }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
          Próximamente
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Aquí se integrarán los casos de prueba, ejecuciones y comentarios
          asociados a este proyecto.
        </Typography>
      </Paper>
    </Box>
  );
};

export default ProjectDetail;
