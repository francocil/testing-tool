// ============================================================
//  FORMULARIO DE MÓDULO (CREAR / EDITAR)
// ============================================================
//
// - Selects predefinidos para tipo_interfaz y tipo_gui
// - Validación básica
// - Manejo de errores 409
//
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";
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
  createModulo,
  getModulo,
  updateModulo,
} from "../../api/modulos";

const tiposInterfaz = [
  "Pantalla",
  "API",
  "SQL",
  "Script",
  "Reporte",
  "Servicio",
  "Microservicio",
  "Batch",
];

const tiposGUI = [
  "Web",
  "Desktop",
  "Mobile",
  "Terminal",
  "Servicio (sin GUI)",
];

const ModuleForm = () => {
  const { id, moduloId } = useParams();
  const isEdit = Boolean(moduloId);

  const navigate = useNavigate();
  const [form, setForm] = useState({
    nombre: "",
    tipo_interfaz: "",
    tipo_gui: "",
    descripcion: "",
  });

  const [loading, setLoading] = useState(false);
  const [loadingModulo, setLoadingModulo] = useState(false);
  const [error, setError] = useState(null);

  // Cargar módulo si es edición
  useEffect(() => {
    const loadModulo = async () => {
      if (!isEdit) return;

      try {
        setLoadingModulo(true);
        const data = await getModulo(moduloId);
        setForm({
          nombre: data.nombre,
          tipo_interfaz: data.tipo_interfaz,
          tipo_gui: data.tipo_gui,
          descripcion: data.descripcion || "",
        });
      } finally {
        setLoadingModulo(false);
      }
    };

    loadModulo();
  }, [moduloId, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleBack = () => {
    navigate(`/proyectos/${id}`);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.nombre.trim()) {
      setError("El nombre es obligatorio.");
      return;
    }

    try {
      setLoading(true);

      const payload = {
        proyecto_id: Number(id),
        nombre: form.nombre.trim(),
        tipo_interfaz: form.tipo_interfaz,
        tipo_gui: form.tipo_gui,
        descripcion: form.descripcion.trim() || null,
      };

      if (isEdit) {
        await updateModulo(moduloId, payload);
      } else {
        await createModulo(payload);
      }

      navigate(`/proyectos/${id}`);
    } catch (err) {
      if (err.response?.status === 409) {
        setError("Ya existe un módulo con ese nombre en este proyecto.");
      } else {
        setError("Error al guardar el módulo.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
        <Button variant="text" startIcon={<ArrowBackIcon />} onClick={handleBack}>
          Volver
        </Button>

        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          {isEdit ? "Editar Módulo" : "Crear Módulo"}
        </Typography>
      </Stack>

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
        {loadingModulo ? (
          <Typography>Cargando módulo...</Typography>
        ) : (
          <form onSubmit={handleSubmit}>
            <Stack spacing={2}>
              <TextField
                label="Nombre del módulo"
                name="nombre"
                value={form.nombre}
                onChange={handleChange}
                fullWidth
                required
              />

              <TextField
                select
                label="Tipo de interfaz"
                name="tipo_interfaz"
                value={form.tipo_interfaz}
                onChange={handleChange}
                fullWidth
                required
              >
                {tiposInterfaz.map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                select
                label="Tipo de GUI"
                name="tipo_gui"
                value={form.tipo_gui}
                onChange={handleChange}
                fullWidth
                required
              >
                {tiposGUI.map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                label="Descripción"
                name="descripcion"
                value={form.descripcion}
                onChange={handleChange}
                fullWidth
                multiline
                minRows={2}
              />

              {error && (
                <Typography color="error" variant="body2">
                  {error}
                </Typography>
              )}

              <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={<SaveIcon />}
                  disabled={loading}
                >
                  {isEdit ? "Guardar cambios" : "Crear módulo"}
                </Button>
              </Box>
            </Stack>
          </form>
        )}
      </Paper>
    </Box>
  );
};

export default ModuleForm;
