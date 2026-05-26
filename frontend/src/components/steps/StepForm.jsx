// ============================================================
// StepForm.jsx (CON ASSERTS AVANZADOS + SIN API_ID EN PASO)
// Formulario institucional para crear/editar un paso
// ============================================================

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Typography,
  Paper,
  IconButton,
  Divider,
} from "@mui/material";

import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";

import axios from "../../api/axiosClient";
import { updateParametro } from "../../api/objeto_parametro";
import {
  getAssertsByPaso,
  createAssert,
  updateAssert,
  deleteAssert,
} from "../../api/paso_assert";

// ------------------------------------------------------------
// Operadores según tipo de assert
// ------------------------------------------------------------
const operatorOptionsByType = {
  jsonpath: [
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "gt",
    "gte",
    "lt",
    "lte",
  ],
  status_code: ["equals", "not_equals", "gt", "gte", "lt", "lte"],
  header: ["equals", "not_equals", "contains", "not_contains"],
  body_contains: ["contains", "not_contains"],
  regex: ["matches_regex"],
  length: ["len_equals", "len_gt", "len_lt"],
};

const StepForm = ({ open, onClose, onSubmit, initialData }) => {
  // ------------------------------------------------------------
  // Normalizar initialData
  // ------------------------------------------------------------
  const emptyData = {
    nombre: "",
    descripcion: "",
    orden: 1,
  };

  const [form, setForm] = useState(initialData || emptyData);
  const [parametros, setParametros] = useState([]);

  // ------------------------------------------------------------
  // ASSERTS
  // ------------------------------------------------------------
  const [asserts, setAsserts] = useState([]);
  const [assertForm, setAssertForm] = useState({
    tipo: "jsonpath",
    expresion: "",
    operador: "equals",
    valor_esperado: "",
    mensaje_error: "",
    orden: 1,
  });
  const [editingAssertId, setEditingAssertId] = useState(null);

  // ------------------------------------------------------------
  // Actualizar form cuando cambia initialData (modo edición)
  // ------------------------------------------------------------
  useEffect(() => {
    setForm(initialData || emptyData);
  }, [initialData]);

  // ------------------------------------------------------------
  // Cargar parámetros SOLO si el paso ya existe
  // ------------------------------------------------------------
  useEffect(() => {
    if (!initialData?.id) return;

    const loadParams = async () => {
      try {
        const res = await axios.get(`/objetos-parametros/by-paso/${initialData.id}`);
        setParametros(res.data);
      } catch (err) {
        console.error("Error cargando parámetros del paso");
      }
    };

    loadParams();
  }, [initialData]);

  // ------------------------------------------------------------
  // Cargar asserts si estamos editando un paso
  // ------------------------------------------------------------
  useEffect(() => {
    if (!initialData?.id) return;

    const loadAsserts = async () => {
      try {
        const res = await getAssertsByPaso(initialData.id);
        setAsserts(res.data || res); // según backend
      } catch (err) {
        console.error("Error cargando asserts");
      }
    };

    loadAsserts();
  }, [initialData]);

  // ------------------------------------------------------------
  // Manejar cambios del formulario principal
  // ------------------------------------------------------------
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ------------------------------------------------------------
  // Manejar cambios del formulario de asserts
  // ------------------------------------------------------------
  const handleAssertChange = (e) => {
    const { name, value } = e.target;

    if (name === "tipo") {
      const ops = operatorOptionsByType[value] || ["equals"];
      setAssertForm((prev) => ({
        ...prev,
        tipo: value,
        operador: ops.includes(prev.operador) ? prev.operador : ops[0],
      }));
      return;
    }

    setAssertForm({ ...assertForm, [name]: value });
  };

  // ------------------------------------------------------------
  // Crear o actualizar assert
  // ------------------------------------------------------------
  const handleSaveAssert = async () => {
    try {
      if (!initialData?.id) {
        alert("Primero debes guardar el paso antes de agregar asserts.");
        return;
      }

      if (editingAssertId) {
        const res = await updateAssert(editingAssertId, assertForm);
        setAsserts((prev) =>
          prev.map((a) => (a.id === editingAssertId ? res : a))
        );
      } else {
        const res = await createAssert({
          ...assertForm,
          paso_id: initialData.id,
        });
        setAsserts((prev) => [...prev, res]);
      }

      // Reset
      setAssertForm({
        tipo: "jsonpath",
        expresion: "",
        operador: "equals",
        valor_esperado: "",
        mensaje_error: "",
        orden: 1,
      });
      setEditingAssertId(null);
    } catch (err) {
      console.error("Error guardando assert", err);
      alert(err?.response?.data?.detail || "Error guardando assert.");
    }
  };

  // ------------------------------------------------------------
  // Editar assert existente
  // ------------------------------------------------------------
  const handleEditAssert = (a) => {
    const ops = operatorOptionsByType[a.tipo] || [a.operador || "equals"];

    setAssertForm({
      tipo: a.tipo,
      expresion: a.expresion || "",
      operador: ops.includes(a.operador) ? a.operador : ops[0],
      valor_esperado: a.valor_esperado || "",
      mensaje_error: a.mensaje_error || "",
      orden: a.orden ?? 1,
    });
    setEditingAssertId(a.id);
  };

  // ------------------------------------------------------------
  // Eliminar assert
  // ------------------------------------------------------------
  const handleDeleteAssert = async (id) => {
    try {
      await deleteAssert(id);
      setAsserts((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      console.error("Error eliminando assert");
    }
  };
  // ------------------------------------------------------------
  // Submit final del paso
  // ------------------------------------------------------------
  const handleSubmit = async () => {
    const payload = {
      ...form,
      parametros: parametros.map((p) => ({
        id: p.id,
        valor_entrada: p.valor_entrada || "",
      })),
    };

    await onSubmit(payload);

    // Guardar parámetros actualizados
    for (const p of parametros) {
      await updateParametro(p.id, { valor_entrada: p.valor_entrada });
    }
  };

  const currentOperatorOptions =
    operatorOptionsByType[assertForm.tipo] || ["equals"];

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>
        {initialData ? "Editar Paso" : "Nuevo Paso"}
      </DialogTitle>

      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          {/* CAMPOS PRINCIPALES */}
          <TextField
            label="Nombre"
            name="nombre"
            value={form.nombre}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            label="Descripción"
            name="descripcion"
            value={form.descripcion}
            onChange={handleChange}
            fullWidth
            multiline
            rows={3}
          />

          <TextField
            label="Orden"
            name="orden"
            type="number"
            value={form.orden}
            onChange={handleChange}
            fullWidth
          />

          {/* PARÁMETROS DEL PASO */}
          {initialData?.id && parametros.length > 0 && (
            <Paper sx={{ p: 2, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                Parámetros del Paso
              </Typography>

              {parametros.map((p) => (
                <TextField
                  key={p.id}
                  label={`${p.nombre} (${p.tipo})`}
                  value={p.valor_entrada || ""}
                  onChange={(e) => {
                    const updated = parametros.map((x) =>
                      x.id === p.id
                        ? { ...x, valor_entrada: e.target.value }
                        : x
                    );
                    setParametros(updated);
                  }}
                  fullWidth
                  sx={{ mb: 2 }}
                />
              ))}
            </Paper>
          )}

          {/* ASSERTS */}
          {initialData?.id && (
            <Paper sx={{ p: 2, mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Asserts del Paso
              </Typography>

              {/* LISTADO */}
              {asserts.map((a) => (
                <Paper
                  key={a.id}
                  sx={{
                    p: 1,
                    mb: 1,
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <div>
                    <Typography>
                      <b>{a.tipo}</b> — {a.expresion}
                    </Typography>
                    <Typography variant="body2">
                      {a.operador} {a.valor_esperado}
                    </Typography>
                  </div>

                  <div>
                    <IconButton onClick={() => handleEditAssert(a)}>
                      <EditIcon />
                    </IconButton>

                    <IconButton onClick={() => handleDeleteAssert(a.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </div>
                </Paper>
              ))}

              <Divider sx={{ my: 2 }} />

              {/* FORMULARIO DE ASSERT */}
              <Typography variant="subtitle1">
                {editingAssertId ? "Editar Assert" : "Nuevo Assert"}
              </Typography>

              <Stack spacing={2} sx={{ mt: 1 }}>
                <FormControl fullWidth>
                  <InputLabel>Tipo</InputLabel>
                  <Select
                    name="tipo"
                    value={assertForm.tipo}
                    label="Tipo"
                    onChange={handleAssertChange}
                  >
                    <MenuItem value="jsonpath">JSONPath</MenuItem>
                    <MenuItem value="status_code">Status Code</MenuItem>
                    <MenuItem value="header">Header</MenuItem>
                    <MenuItem value="body_contains">Body Contains</MenuItem>
                    <MenuItem value="regex">Regex</MenuItem>
                    <MenuItem value="length">Length</MenuItem>
                  </Select>
                </FormControl>

                <TextField
                  label="Expresión (JSONPath, header, etc.)"
                  name="expresion"
                  value={assertForm.expresion}
                  onChange={handleAssertChange}
                  fullWidth
                />

                <FormControl fullWidth>
                  <InputLabel>Operador</InputLabel>
                  <Select
                    name="operador"
                    value={assertForm.operador}
                    label="Operador"
                    onChange={handleAssertChange}
                  >
                    {currentOperatorOptions.map((op) => (
                      <MenuItem key={op} value={op}>
                        {op}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <TextField
                  label="Valor esperado"
                  name="valor_esperado"
                  value={assertForm.valor_esperado}
                  onChange={handleAssertChange}
                  fullWidth
                />

                <TextField
                  label="Mensaje de error"
                  name="mensaje_error"
                  value={assertForm.mensaje_error}
                  onChange={handleAssertChange}
                  fullWidth
                />

                <TextField
                  label="Orden"
                  name="orden"
                  type="number"
                  value={assertForm.orden}
                  onChange={handleAssertChange}
                  fullWidth
                />

                <Button variant="contained" onClick={handleSaveAssert}>
                  {editingAssertId ? "Actualizar Assert" : "Agregar Assert"}
                </Button>
              </Stack>
            </Paper>
          )}
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button variant="contained" onClick={handleSubmit}>
          Guardar Paso
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default StepForm;
