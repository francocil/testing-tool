import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  MenuItem,
} from "@mui/material";

import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import SaveIcon from "@mui/icons-material/Save";

import {
  createCasoPrueba,
  getCasoPrueba,
  updateCasoPrueba,
} from "../../api/casosPrueba";

const CaseForm = () => {
  const { id, moduloId, casoId } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(casoId);

  const [form, setForm] = useState({
    nombre: "",
    objetivo: "",
    descripcion: "",
    precondiciones: "",
    postcondiciones: "",
    estado: "activo",
    porcentaje_aceptacion: "",
  });

  const [loading, setLoading] = useState(isEdit);
  const [error, setError] = useState(null);

  // ------------------------------------------------------------
  // Cargar datos si es edición
  // ------------------------------------------------------------
  useEffect(() => {
    const load = async () => {
      if (!isEdit) return;

      try {
        const data = await getCasoPrueba(casoId);

        setForm({
          nombre: data.nombre || "",
          objetivo: data.objetivo || "",
          descripcion: data.descripcion || "",
          precondiciones: data.precondiciones || "",
          postcondiciones: data.postcondiciones || "",
          estado: data.estado || "activo",
          porcentaje_aceptacion:
            data.porcentaje_aceptacion != null
              ? String(data.porcentaje_aceptacion)
              : "",
        });

        setError(null);
      } catch (err) {
        console.error(err);
        setError("No se pudo cargar el caso de prueba.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [isEdit, casoId]);

  // ------------------------------------------------------------
  // Navegación corregida
  // ------------------------------------------------------------
  const handleBack = () => {
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos`);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ------------------------------------------------------------
  // Guardar
  // ------------------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      modulo_id: Number(moduloId),
      nombre: form.nombre.trim(),
      objetivo: form.objetivo.trim() || null,
      descripcion: form.descripcion.trim() || null,
      precondiciones: form.precondiciones.trim() || null,
      postcondiciones: form.postcondiciones.trim() || null,
      estado: form.estado,
      porcentaje_aceptacion:
        form.porcentaje_aceptacion !== ""
          ? Number(form.porcentaje_aceptacion)
          : null,
    };

    try {
      setError(null);

      if (isEdit) {
        await updateCasoPrueba(casoId, payload);
      } else {
        await createCasoPrueba(payload);
      }

      navigate(`/proyectos/${id}/modulos/${moduloId}/casos`);
    } catch (err) {
      console.error(err);

      if (err.response?.status === 409) {
        setError("Ya existe un caso de prueba con ese nombre en este módulo.");
      } else {
        setError("Ocurrió un error al guardar el caso de prueba.");
      }
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Cargando caso de prueba...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Encabezado */}
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
            {isEdit ? "Editar Caso de Prueba" : "Nuevo Caso de Prueba"}
          </Typography>
        </Stack>
      </Stack>

      {/* Formulario */}
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
        <form onSubmit={handleSubmit}>
          <Stack spacing={2}>
            <TextField
              label="Nombre del caso de prueba"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              required
              fullWidth
            />

            <TextField
              label="Objetivo general"
              name="objetivo"
              value={form.objetivo}
              onChange={handleChange}
              multiline
              minRows={2}
              fullWidth
            />

            <TextField
              label="Descripción detallada"
              name="descripcion"
              value={form.descripcion}
              onChange={handleChange}
              multiline
              minRows={3}
              fullWidth
            />

            <TextField
              label="Precondiciones"
              name="precondiciones"
              value={form.precondiciones}
              onChange={handleChange}
              multiline
              minRows={2}
              fullWidth
            />

            <TextField
              label="Postcondiciones"
              name="postcondiciones"
              value={form.postcondiciones}
              onChange={handleChange}
              multiline
              minRows={2}
              fullWidth
            />

            <TextField
              select
              label="Estado"
              name="estado"
              value={form.estado}
              onChange={handleChange}
              fullWidth
            >
              <MenuItem value="activo">Activo</MenuItem>
              <MenuItem value="inactivo">Inactivo</MenuItem>
              <MenuItem value="borrador">Borrador</MenuItem>
            </TextField>

            <TextField
              label="Porcentaje de aceptación (%)"
              name="porcentaje_aceptacion"
              value={form.porcentaje_aceptacion}
              onChange={handleChange}
              type="number"
              inputProps={{ min: 0, max: 100, step: 1 }}
              fullWidth
            />

            {error && (
              <Typography color="error" variant="body2">
                {error}
              </Typography>
            )}

            <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
              <Button type="submit" variant="contained" startIcon={<SaveIcon />}>
                {isEdit ? "Guardar cambios" : "Crear caso"}
              </Button>
            </Box>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
};

export default CaseForm;
