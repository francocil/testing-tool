// ============================================================
//  FORMULARIO DE PROYECTO - CREAR / EDITAR (CON INSTITUCIONAL)
//  🔥 PROTEGIDO POR PERMISOS INSTITUCIONALES
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Stack,
  MenuItem,
} from "@mui/material";

import SaveIcon from "@mui/icons-material/Save";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

import {
  createProyecto,
  getProyecto,
  updateProyecto,
} from "../../api/proyectos";

import { getReparticiones } from "../../api/reparticiones";
import { getDirecciones } from "../../api/direcciones";
import { getAreas } from "../../api/areas";

// 🔥 PERMISOS INSTITUCIONALES
import { usePermission } from "../../context/PermissionContext";

const emptyForm = {
  nombre: "",
  objetivo_general: "",
  contexto: "",
  reparticion_id: "",
  direccion_id: "",
  area_id: "",
};

const ProjectForm = () => {
  const { id } = useParams();
  const isEdit = Boolean(id);

  const { can } = usePermission(); // 🔥 permisos

  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);
  const [loadingProyecto, setLoadingProyecto] = useState(false);
  const [error, setError] = useState(null);

  const [reparticiones, setReparticiones] = useState([]);
  const [direcciones, setDirecciones] = useState([]);
  const [areas, setAreas] = useState([]);

  const navigate = useNavigate();

  // ============================================================
  // 🔥 PROTECCIÓN DE ACCESO
  // ============================================================
  if (isEdit && !can("editar_proyectos")) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h4" color="error" fontWeight={700}>
          Acceso denegado
        </Typography>
        <Typography sx={{ mt: 1 }}>
          No tenés permiso para editar proyectos.
        </Typography>
      </Box>
    );
  }

  if (!isEdit && !can("crear_proyectos")) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h4" color="error" fontWeight={700}>
          Acceso denegado
        </Typography>
        <Typography sx={{ mt: 1 }}>
          No tenés permiso para crear proyectos.
        </Typography>
      </Box>
    );
  }

  // =================================================
  // CARGA INICIAL DE REPARTICIONES
  // =================================================
  const loadReparticiones = async () => {
    const data = await getReparticiones();
    setReparticiones(data);
  };

  // =================================================
  // CARGA DINÁMICA DE DIRECCIONES
  // =================================================
  const loadDirecciones = async (reparticion_id) => {
    if (!reparticion_id) {
      setDirecciones([]);
      return;
    }
    const data = await getDirecciones({ reparticion_id });
    setDirecciones(data);
  };

  // =================================================
  // CARGA DINÁMICA DE ÁREAS
  // =================================================
  const loadAreas = async (direccion_id) => {
    if (!direccion_id) {
      setAreas([]);
      return;
    }
    const data = await getAreas({ direccion_id });
    setAreas(data);
  };

  // =================================================
  // CARGA DE PROYECTO EN MODO EDICIÓN
  // =================================================
  useEffect(() => {
    loadReparticiones();

    const loadProyectoData = async () => {
      if (!isEdit) return;

      try {
        setLoadingProyecto(true);
        const data = await getProyecto(id);

        setForm({
          nombre: data.nombre || "",
          objetivo_general: data.objetivo_general || "",
          contexto: data.contexto || "",
          reparticion_id: data.reparticion_id || "",
          direccion_id: data.direccion_id || "",
          area_id: data.area_id || "",
        });

        if (data.reparticion_id) {
          await loadDirecciones(data.reparticion_id);
        }
        if (data.direccion_id) {
          await loadAreas(data.direccion_id);
        }

        setError(null);
      } catch (err) {
        console.error(err);
        setError("No se pudo cargar el proyecto.");
      } finally {
        setLoadingProyecto(false);
      }
    };

    loadProyectoData();
  }, [id, isEdit]);

  // ========================================
  // HANDLE CHANGE
  // ========================================
  const handleChange = async (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (name === "reparticion_id") {
      setForm((prev) => ({
        ...prev,
        direccion_id: "",
        area_id: "",
      }));
      await loadDirecciones(value);
      setAreas([]);
    }

    if (name === "direccion_id") {
      setForm((prev) => ({
        ...prev,
        area_id: "",
      }));
      await loadAreas(value);
    }
  };

  // ========================================
  // SUBMIT (PROTEGIDO)
  // ========================================
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.nombre.trim()) {
      setError("El nombre del proyecto es obligatorio.");
      return;
    }

    // 🔥 Protección adicional en submit
    if (isEdit && !can("editar_proyectos")) {
      alert("No tenés permiso para editar proyectos.");
      return;
    }

    if (!isEdit && !can("crear_proyectos")) {
      alert("No tenés permiso para crear proyectos.");
      return;
    }

    try {
      setLoading(true);

      const payload = {
        nombre: form.nombre.trim(),
        objetivo_general: form.objetivo_general.trim() || null,
        contexto: form.contexto.trim() || null,
        reparticion_id: form.reparticion_id || null,
        direccion_id: form.direccion_id || null,
        area_id: form.area_id || null,
      };

      if (isEdit) {
        await updateProyecto(id, payload);
      } else {
        await createProyecto(payload);
      }

      navigate("/proyectos");
    } catch (err) {
      console.error(err);

      if (err.response?.status === 409) {
        setError(err.response.data?.detail || "Nombre de proyecto duplicado.");
      } else {
        setError("Ocurrió un error al guardar el proyecto.");
      }
    } finally {
      setLoading(false);
    }
  };

  // ==============================
  // RENDER
  // ==============================
  return (
    <Box sx={{ p: 3 }}>
      {/* HEADER */}
      <Box
        sx={{
          mb: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Stack direction="row" spacing={2} alignItems="center">
          <Button
            variant="text"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate("/proyectos")}
          >
            Volver
          </Button>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            {isEdit ? "Editar Proyecto" : "Crear Proyecto"}
          </Typography>
        </Stack>
      </Box>

      {/* FORM */}
      <Paper
        elevation={3}
        sx={{
          p: 3,
          borderRadius: 3,
          maxWidth: 700,
          background: (theme) =>
            theme.palette.mode === "light"
              ? "rgba(255,255,255,0.85)"
              : "rgba(15,15,15,0.9)",
          backdropFilter: "blur(10px)",
        }}
      >
        {loadingProyecto ? (
          <Typography>Cargando datos del proyecto...</Typography>
        ) : (
          <form onSubmit={handleSubmit}>
            <Stack spacing={2}>
              {/* NOMBRE */}
              <TextField
                label="Nombre del proyecto"
                name="nombre"
                value={form.nombre}
                onChange={handleChange}
                fullWidth
                required
              />

              {/* OBJETIVO */}
              <TextField
                label="Objetivo general"
                name="objetivo_general"
                value={form.objetivo_general}
                onChange={handleChange}
                fullWidth
                multiline
                minRows={2}
              />

              {/* CONTEXTO */}
              <TextField
                label="Contexto"
                name="contexto"
                value={form.contexto}
                onChange={handleChange}
                fullWidth
                multiline
                minRows={2}
              />

              {/* SELECT INSTITUCIONAL: REPARTICIÓN */}
              <TextField
                select
                label="Repartición"
                name="reparticion_id"
                value={form.reparticion_id}
                onChange={handleChange}
                fullWidth
              >
                <MenuItem value="">Sin asignar</MenuItem>
                {reparticiones.map((r) => (
                  <MenuItem key={r.id} value={r.id}>
                    {r.nombre}
                  </MenuItem>
                ))}
              </TextField>

              {/* SELECT DIRECCIÓN */}
              <TextField
                select
                label="Dirección"
                name="direccion_id"
                value={form.direccion_id}
                onChange={handleChange}
                fullWidth
                disabled={!form.reparticion_id}
              >
                <MenuItem value="">Sin asignar</MenuItem>
                {direcciones.map((d) => (
                  <MenuItem key={d.id} value={d.id}>
                    {d.nombre}
                  </MenuItem>
                ))}
              </TextField>

              {/* SELECT ÁREA */}
              <TextField
                select
                label="Área"
                name="area_id"
                value={form.area_id}
                onChange={handleChange}
                fullWidth
                disabled={!form.direccion_id}
              >
                <MenuItem value="">Sin asignar</MenuItem>
                {areas.map((a) => (
                  <MenuItem key={a.id} value={a.id}>
                    {a.nombre}
                  </MenuItem>
                ))}
              </TextField>

              {/* ERROR */}
              {error && (
                <Typography color="error" variant="body2">
                  {error}
                </Typography>
              )}

              {/* BOTÓN GUARDAR (PROTEGIDO) */}
              <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
                {(isEdit ? can("editar_proyectos") : can("crear_proyectos")) && (
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    startIcon={<SaveIcon />}
                    disabled={loading}
                  >
                    {isEdit ? "Guardar cambios" : "Crear proyecto"}
                  </Button>
                )}
              </Box>
            </Stack>
          </form>
        )}
      </Paper>
    </Box>
  );
};

export default ProjectForm;
