// ============================================================
//  GESTIÓN DE AGENTES - VERSION PRO FUSIONADA + PERMISOS REALES
// ============================================================

import { useEffect, useState, useRef, useMemo } from "react";
import { FormControl, FormLabel } from "@mui/material";
import {
  Box,
  Typography,
  Paper,
  Stack,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  TablePagination,
  Skeleton,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import {
  getAgentes,
  createAgente,
  updateAgente,
  deleteAgente,
  obtenerAgente,
} from "../../api/agentes";

import { getReparticiones } from "../../api/reparticiones";
import { getDirecciones } from "../../api/direcciones";
import { getAreas } from "../../api/areas";

import usePermission from "../../hooks/usePermission";

const Agentes = () => {
  // ============================================================
  // PERMISOS INSTITUCIONALES
  // ============================================================
  const { can } = usePermission();

  const puedeVer = can("seguridad_usuario_ver");
  const puedeCrear = can("seguridad_usuario_crear");
  const puedeEditar = can("seguridad_usuario_editar");
  const puedeEliminar = can("seguridad_usuario_eliminar");

  // Si NO puede ver, no mostramos nada
  if (!puedeVer) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h6" color="error">
          No tenés permisos para ver agentes.
        </Typography>
      </Box>
    );
  }

  // ============================================================
  // ESTADOS
  // ============================================================
  const [agentes, setAgentes] = useState([]);
  const [loading, setLoading] = useState(true);

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const [filtros, setFiltros] = useState({
    texto: "",
    reparticion_id: "",
    direccion_id: "",
    area_id: "",
  });

  const [reparticiones, setReparticiones] = useState([]);
  const [direccionesFiltro, setDireccionesFiltro] = useState([]);
  const [areasFiltro, setAreasFiltro] = useState([]);

  const [direccionesForm, setDireccionesForm] = useState([]);
  const [areasForm, setAreasForm] = useState([]);

  const [open, setOpen] = useState(false);
  const [openView, setOpenView] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);

  const [editMode, setEditMode] = useState(false);
  const [selected, setSelected] = useState(null);
  const [deleteTarget, setDeleteTarget] = useState(null);

  const [form, setForm] = useState({});
  const [errors, setErrors] = useState({});
  const [detalle, setDetalle] = useState(null);

  const cuilRef = useRef(null);

  // ============================================================
  // VALIDACIONES
  // ============================================================
  const validarCuil = (cuil) => {
    if (!cuil) return false;
    const limpio = cuil.replace(/-/g, "").trim();
    if (!/^\d+$/.test(limpio)) return false;
    if (limpio.length !== 11) return false;
    const prefijo = limpio.slice(0, 2);
    if (!["20", "27", "23", "24", "30"].includes(prefijo)) return false;
    return true;
  };

  const generoPorCuil = (cuil) => {
    const limpio = cuil.replace(/-/g, "").trim();
    if (limpio.length !== 11) return "";
    const prefijo = limpio.slice(0, 2);
    if (prefijo === "20") return "masculino";
    if (prefijo === "27") return "femenino";
    return "";
  };

  // ============================================================
  // LOAD DATA
  // ============================================================
  useEffect(() => {
    const load = async () => {
      setLoading(true);

      const [ags, reps] = await Promise.all([
        getAgentes(),
        getReparticiones(),
      ]);

      setAgentes(ags);
      setReparticiones(reps);
      setLoading(false);
    };

    load();
  }, []);

  // ============================================================
  // FORM HELPERS
  // ============================================================
  const loadDireccionesForm = async (reparticionId) => {
    if (!reparticionId) {
      setDireccionesForm([]);
      return;
    }
    const dirs = await getDirecciones({ reparticion_id: reparticionId });
    setDireccionesForm(dirs);
  };

  const loadAreasForm = async (direccionId) => {
    if (!direccionId) {
      setAreasForm([]);
      return;
    }
    const ars = await getAreas({ direccion_id: direccionId });
    setAreasForm(ars);
  };

  // ============================================================
  // VALIDACIÓN DE FORMULARIO
  // ============================================================
  const validateForm = () => {
    const e = {};

    if (!form.cuil || !validarCuil(form.cuil)) e.cuil = "CUIL inválido";
    if (!form.apellido_nombre) e.apellido_nombre = "Campo obligatorio";
    if (!form.email) e.email = "Campo obligatorio";
    if (!form.reparticion_id) e.reparticion_id = "Campo obligatorio";
    if (!form.direccion_id) e.direccion_id = "Campo obligatorio";
    if (!form.area_id) e.area_id = "Campo obligatorio";

    setErrors(e);
    return Object.keys(e).length === 0;
  };

  // ============================================================
  // FILTRADO OPTIMIZADO
  // ============================================================
  const agentesFiltrados = useMemo(() => {
    return agentes.filter((a) => {
      const t = filtros.texto.toLowerCase();

      return (
        (!t ||
          a.dni.toString().includes(t) ||
          a.apellido_nombre.toLowerCase().includes(t) ||
          a.email.toLowerCase().includes(t)) &&
        (!filtros.reparticion_id ||
          a.reparticion_id === Number(filtros.reparticion_id)) &&
        (!filtros.direccion_id ||
          a.direccion_id === Number(filtros.direccion_id)) &&
        (!filtros.area_id ||
          a.area_id === Number(filtros.area_id))
      );
    });
  }, [agentes, filtros]);

  // ============================================================
  // PAGINACIÓN
  // ============================================================
  const paginatedAgentes = useMemo(() => {
    const start = page * rowsPerPage;
    return agentesFiltrados.slice(start, start + rowsPerPage);
  }, [agentesFiltrados, page, rowsPerPage]);

  // ============================================================
  // FILTROS DINÁMICOS
  // ============================================================
  useEffect(() => {
    if (filtros.reparticion_id) {
      getDirecciones({ reparticion_id: filtros.reparticion_id }).then(setDireccionesFiltro);
      setFiltros((prev) => ({ ...prev, direccion_id: "", area_id: "" }));
      setAreasFiltro([]);
    }
  }, [filtros.reparticion_id]);

  useEffect(() => {
    if (filtros.direccion_id) {
      getAreas({ direccion_id: filtros.direccion_id }).then(setAreasFiltro);
      setFiltros((prev) => ({ ...prev, area_id: "" }));
    }
  }, [filtros.direccion_id]);
  // ============================================================
  // HANDLERS
  // ============================================================
  const handleOpenCreate = () => {
    if (!puedeCrear) return;

    setEditMode(false);
    setErrors({});
    setForm({
      dni: "",
      cuil: "",
      apellido_nombre: "",
      email: "",
      reparticion_id: "",
      direccion_id: "",
      area_id: "",
      cargo: "",
      genero: "",
    });

    setDireccionesForm([]);
    setAreasForm([]);

    setOpen(true);
  };

  const handleOpenEdit = async (agente) => {
    if (!puedeEditar) return;

    setEditMode(true);
    setSelected(agente.id);
    setErrors({});

    await loadDireccionesForm(agente.reparticion_id);
    await loadAreasForm(agente.direccion_id);

    setForm({
      dni: agente.dni,
      cuil: agente.cuil || "",
      apellido_nombre: agente.apellido_nombre,
      email: agente.email,
      reparticion_id: agente.reparticion_id,
      direccion_id: agente.direccion_id,
      area_id: agente.area_id,
      cargo: agente.cargo,
      genero: agente.genero || generoPorCuil(agente.cuil || ""),
    });

    setOpen(true);
  };

  const handleOpenView = async (id) => {
    if (!puedeVer) return;

    const data = await obtenerAgente(id);

    await loadDireccionesForm(data.reparticion_id);
    await loadAreasForm(data.direccion_id);

    const rep = reparticiones.find((r) => r.id === data.reparticion_id);
    const dir = direccionesForm.find((d) => d.id === data.direccion_id);
    const ar = areasForm.find((a) => a.id === data.area_id);

    setDetalle({
      ...data,
      reparticion_nombre: rep?.nombre || "",
      direccion_nombre: dir?.nombre || "",
      area_nombre: ar?.nombre || "",
    });

    setOpenView(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelected(null);
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      const payload = { ...form };

      if (editMode) {
        if (!puedeEditar) return;
        await updateAgente(selected, payload);
      } else {
        if (!puedeCrear) return;
        await createAgente(payload);
      }

      handleClose();
      const updated = await getAgentes();
      setAgentes(updated);
    } catch (error) {
      const status = error.response?.status;

      if (status === 401) {
        setErrors({ global: "Sesión expirada. Volvé a iniciar sesión." });
      } else if (status === 422) {
        setErrors({ global: "Datos inválidos. Revisá el formulario." });
      } else if (status === 409) {
        setErrors({
          global: "DNI, CUIL o Email ya existen en el sistema.",
        });
      } else {
        setErrors({ global: "Error inesperado al guardar el agente." });
      }
    }
  };

  const handleOpenDelete = (agente) => {
    if (!puedeEliminar) return;
    setDeleteTarget(agente);
    setOpenDelete(true);
  };

  const handleConfirmDelete = async () => {
    if (!puedeEliminar) return;

    try {
      await deleteAgente(deleteTarget.id);
      setOpenDelete(false);
      setDeleteTarget(null);

      const updated = await getAgentes();
      setAgentes(updated);
    } catch (error) {
      alert("Error al eliminar el agente.");
    }
  };

  const handleCancelDelete = () => {
    setOpenDelete(false);
    setDeleteTarget(null);
  };

  // ============================================================
  // LOADING UI
  // ============================================================
  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        {[...Array(6)].map((_, i) => (
          <Skeleton key={i} height={50} sx={{ mb: 1 }} />
        ))}
      </Box>
    );
  }

  // ============================================================
  // RENDER PRINCIPAL
  // ============================================================
  return (
    <Box sx={{ p: 3 }}>
      {/* ENCABEZADO */}
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        sx={{ mb: 3 }}
      >
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Gestión de Agentes
        </Typography>

        {puedeCrear && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleOpenCreate}
          >
            Nuevo Agente
          </Button>
        )}
      </Stack>

      {/* FILTROS */}
      <Paper elevation={3} sx={{ p: 2, mb: 3, borderRadius: 3 }}>
        <Stack direction="row" spacing={2}>
          <TextField
            label="Buscar (DNI, Nombre, Email)"
            value={filtros.texto}
            onChange={(e) =>
              setFiltros({ ...filtros, texto: e.target.value })
            }
            fullWidth
            autoComplete="off"
            disabled={open}
          />

          <TextField
            select
            label="Repartición"
            value={filtros.reparticion_id}
            onChange={(e) =>
              setFiltros({ ...filtros, reparticion_id: e.target.value })
            }
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="">Todas</MenuItem>
            {reparticiones.map((r) => (
              <MenuItem key={r.id} value={r.id}>
                {r.nombre}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            select
            label="Dirección"
            value={filtros.direccion_id}
            onChange={(e) =>
              setFiltros({ ...filtros, direccion_id: e.target.value })
            }
            sx={{ minWidth: 200 }}
            disabled={!filtros.reparticion_id}
          >
            <MenuItem value="">Todas</MenuItem>
            {direccionesFiltro.map((d) => (
              <MenuItem key={d.id} value={d.id}>
                {d.nombre}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            select
            label="Área"
            value={filtros.area_id}
            onChange={(e) =>
              setFiltros({ ...filtros, area_id: e.target.value })
            }
            sx={{ minWidth: 200 }}
            disabled={!filtros.direccion_id}
          >
            <MenuItem value="">Todas</MenuItem>
            {areasFiltro.map((a) => (
              <MenuItem key={a.id} value={a.id}>
                {a.nombre}
              </MenuItem>
            ))}
          </TextField>
        </Stack>
      </Paper>

      {/* TABLA */}
      <Paper elevation={3} sx={{ p: 3, borderRadius: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Listado de Agentes
        </Typography>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>DNI</strong></TableCell>
              <TableCell><strong>Apellido y Nombre</strong></TableCell>
              <TableCell><strong>Email</strong></TableCell>
              <TableCell><strong>Acciones</strong></TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {paginatedAgentes.map((a) => (
              <TableRow key={a.id} hover>
                <TableCell>{a.dni}</TableCell>
                <TableCell>{a.apellido_nombre}</TableCell>
                <TableCell>{a.email}</TableCell>

                <TableCell>
                  <Stack direction="row" spacing={1}>
                    {puedeVer && (
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<VisibilityIcon />}
                        onClick={() => handleOpenView(a.id)}
                      >
                        Ver
                      </Button>
                    )}

                    {puedeEditar && (
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<EditIcon />}
                        onClick={() => handleOpenEdit(a)}
                      >
                        Editar
                      </Button>
                    )}

                    {puedeEliminar && (
                      <Button
                        variant="outlined"
                        color="error"
                        size="small"
                        startIcon={<DeleteIcon />}
                        onClick={() => handleOpenDelete(a)}
                      >
                        Eliminar
                      </Button>
                    )}
                  </Stack>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        {/* PAGINACIÓN */}
        <TablePagination
          component="div"
          count={agentesFiltrados.length}
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
      {/* MODAL DE CREACIÓN / EDICIÓN */}
      <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
        <DialogTitle
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
            pb: 1,
          }}
        >
          <AccountCircleIcon color="primary" />
          {editMode ? "Editar Agente" : "Nuevo Agente"}
        </DialogTitle>

        <DialogContent sx={{ mt: 1 }}>
          <Stack spacing={2}>
            {errors.global && (
              <Alert severity="error">{errors.global}</Alert>
            )}

            {/* CUIL */}
            <TextField
              inputRef={cuilRef}
              label="CUIL"
              value={form.cuil || ""}
              onChange={(e) => {
                const value = e.target.value;
                const limpio = value.replace(/-/g, "");

                let dniExtraido = "";
                if (limpio.length >= 10) {
                  dniExtraido = limpio.substring(2, 10);
                }

                setForm({
                  ...form,
                  cuil: value,
                  dni: dniExtraido,
                  genero: generoPorCuil(value),
                });

                setErrors((prev) => ({
                  ...prev,
                  cuil: undefined,
                  dni: undefined,
                }));
              }}
              onBlur={() => {
                if (!validarCuil(form.cuil)) {
                  setErrors((prev) => ({
                    ...prev,
                    cuil: "CUIL inválido",
                  }));
                  setTimeout(() => cuilRef.current?.focus(), 0);
                }
              }}
              fullWidth
              error={Boolean(errors.cuil)}
              helperText={errors.cuil}
            />

            {/* DNI */}
            <TextField
              label="DNI"
              value={form.dni || ""}
              fullWidth
              InputProps={{ readOnly: true }}
              error={Boolean(errors.dni)}
              helperText={errors.dni}
            />

            {/* GÉNERO */}
            <TextField
              label="Género"
              value={form.genero || ""}
              fullWidth
              InputProps={{ readOnly: true }}
            />

            {/* NOMBRE */}
            <TextField
              label="Apellido, Nombre"
              value={form.apellido_nombre || ""}
              onChange={(e) =>
                setForm({ ...form, apellido_nombre: e.target.value })
              }
              fullWidth
              error={Boolean(errors.apellido_nombre)}
              helperText={errors.apellido_nombre}
            />

            {/* EMAIL */}
            <TextField
              label="Email"
              value={form.email || ""}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              fullWidth
              error={Boolean(errors.email)}
              helperText={errors.email}
            />

            {/* REPARTICIÓN */}
            <TextField
              select
              label="Repartición"
              value={form.reparticion_id || ""}
              onChange={async (e) => {
                const value = e.target.value;
                setForm({
                  ...form,
                  reparticion_id: value,
                  direccion_id: "",
                  area_id: "",
                });
                await loadDireccionesForm(value);
                setAreasForm([]);
                setErrors((prev) => ({
                  ...prev,
                  reparticion_id: undefined,
                  direccion_id: undefined,
                  area_id: undefined,
                }));
              }}
              fullWidth
              error={Boolean(errors.reparticion_id)}
              helperText={errors.reparticion_id}
            >
              {reparticiones.map((r) => (
                <MenuItem key={r.id} value={r.id}>
                  {r.nombre}
                </MenuItem>
              ))}
            </TextField>

            {/* DIRECCIÓN */}
            <TextField
              select
              label="Dirección"
              value={form.direccion_id || ""}
              onChange={async (e) => {
                const value = e.target.value;
                setForm({ ...form, direccion_id: value, area_id: "" });
                await loadAreasForm(value);
                setErrors((prev) => ({
                  ...prev,
                  direccion_id: undefined,
                  area_id: undefined,
                }));
              }}
              fullWidth
              disabled={!form.reparticion_id}
              error={Boolean(errors.direccion_id)}
              helperText={errors.direccion_id}
            >
              {direccionesForm.map((d) => (
                <MenuItem key={d.id} value={d.id}>
                  {d.nombre}
                </MenuItem>
              ))}
            </TextField>

            {/* ÁREA */}
            <TextField
              select
              label="Área"
              value={form.area_id || ""}
              onChange={(e) =>
                setForm({ ...form, area_id: e.target.value })
              }
              fullWidth
              disabled={!form.direccion_id}
              error={Boolean(errors.area_id)}
              helperText={errors.area_id}
            >
              {areasForm.map((a) => (
                <MenuItem key={a.id} value={a.id}>
                  {a.nombre}
                </MenuItem>
              ))}
            </TextField>

            {/* CARGO */}
            <TextField
              label="Cargo"
              value={form.cargo || ""}
              onChange={(e) => setForm({ ...form, cargo: e.target.value })}
              fullWidth
              error={Boolean(errors.cargo)}
              helperText={errors.cargo}
            />
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleClose}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit}>
            Guardar
          </Button>
        </DialogActions>
      </Dialog>

      {/* MODAL DE DETALLE */}
      <Dialog
        open={openView}
        onClose={() => setOpenView(false)}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle
          sx={{
            display: "flex",
            alignItems: "flex-start",
            gap: 1,
            pb: 1,
          }}
        >
          <VisibilityIcon color="primary" />
          Información del Agente
        </DialogTitle>

        <DialogContent sx={{ paddingTop: 3 }}>
          {detalle && (
            <Stack spacing={2}>
              <FormControl fullWidth>
                <FormLabel sx={{ mb: 0.5 }}>DNI</FormLabel>
                <TextField
                  value={detalle.dni}
                  fullWidth
                  InputProps={{ readOnly: true }}
                  variant="outlined"
                />
              </FormControl>

              <TextField
                label="CUIL"
                value={detalle.cuil || ""}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Género"
                value={detalle.genero || ""}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Apellido y Nombre"
                value={detalle.apellido_nombre}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Email"
                value={detalle.email}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Cargo"
                value={detalle.cargo}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Repartición"
                value={detalle.reparticion_nombre}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Dirección"
                value={detalle.direccion_nombre}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Área"
                value={detalle.area_nombre}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              <TextField
                label="Fecha de creación"
                value={detalle.fecha_creacion?.substring(0, 10) || ""}
                fullWidth
                InputProps={{ readOnly: true }}
                InputLabelProps={{ shrink: true }}
              />

              {detalle.fecha_baja && (
                <TextField
                  label="Fecha de baja"
                  value={detalle.fecha_baja.substring(0, 10)}
                  fullWidth
                  InputProps={{ readOnly: true }}
                  InputLabelProps={{ shrink: true }}
                />
              )}
            </Stack>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setOpenView(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>

      {/* MODAL DE CONFIRMACIÓN DE ELIMINACIÓN */}
      <Dialog open={openDelete} onClose={handleCancelDelete}>
        <DialogTitle>Confirmar eliminación</DialogTitle>
        <DialogContent>
          ¿Seguro que querés eliminar al agente{" "}
          <strong>{deleteTarget?.apellido_nombre}</strong>?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete}>Cancelar</Button>
          <Button color="error" variant="contained" onClick={handleConfirmDelete}>
            Eliminar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Agentes;
