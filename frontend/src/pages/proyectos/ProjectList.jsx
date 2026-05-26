// ============================================================
//  LISTADO DE PROYECTOS (con sidebar de filtros institucionales PRO)
// ============================================================
//
// - Filtros institucionales: Repartición → Dirección → Área
// - Filtros existentes: nombre, estado, sort
// - Drawer lateral DESPLEGABLE
// - Paginación real desde backend
// - Ordenamiento dinámico
// - Diseño institucional glass
// - 🔥 Protección institucional por permisos (crear, editar, eliminar, ver)
//
// ============================================================

import { useEffect, useState } from "react";
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
  TablePagination,
  Skeleton,
  Drawer,
  TextField,
  MenuItem,
  IconButton,
} from "@mui/material";

import FilterListIcon from "@mui/icons-material/FilterList";
import AddIcon from "@mui/icons-material/Add";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { useNavigate } from "react-router-dom";

import { getProyectos, deleteProyecto } from "../../api/proyectos";
import { getReparticiones } from "../../api/reparticiones";
import { getDirecciones } from "../../api/direcciones";
import { getAreas } from "../../api/areas";

// 🔥 PERMISOS INSTITUCIONALES
import { usePermission } from "../../context/PermissionContext";

const ProjectList = () => {
  const navigate = useNavigate();
  const { can } = usePermission(); // 🔥 permisos

  // =============================
  // ESTADOS
  // =============================
  const [proyectos, setProyectos] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filtros
  const [nombre, setNombre] = useState("");
  const [estado, setEstado] = useState("");
  const [sort, setSort] = useState("fecha_creacion:desc");

  // Filtros institucionales
  const [reparticionId, setReparticionId] = useState("");
  const [direccionId, setDireccionId] = useState("");
  const [areaId, setAreaId] = useState("");

  const [reparticiones, setReparticiones] = useState([]);
  const [direcciones, setDirecciones] = useState([]);
  const [areas, setAreas] = useState([]);

  // Drawer lateral
  const [openFilters, setOpenFilters] = useState(false);

  // Paginación real
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);

  // =============================
  // CARGA INICIAL DE INSTITUCIONAL
  // =============================
  const loadReparticiones = async () => {
    const data = await getReparticiones();
    setReparticiones(data);
  };

  const loadDirecciones = async (repId) => {
    if (!repId) {
      setDirecciones([]);
      return;
    }
    const data = await getDirecciones({ reparticion_id: repId });
    setDirecciones(data);
  };

  const loadAreas = async (dirId) => {
    if (!dirId) {
      setAreas([]);
      return;
    }
    const data = await getAreas({ direccion_id: dirId });
    setAreas(data);
  };

  useEffect(() => {
    loadReparticiones();
  }, []);

  // =============================
  // LOAD DATA (con filtros)
  // =============================
  const load = async () => {
    setLoading(true);

    const params = {
      limit: rowsPerPage,
      offset: page * rowsPerPage,
      sort,
    };

    if (nombre.trim() !== "") params.nombre = nombre;
    if (estado !== "") params.estado = estado;

    if (reparticionId) params.reparticion_id = reparticionId;
    if (direccionId) params.direccion_id = direccionId;
    if (areaId) params.area_id = areaId;

    const data = await getProyectos(params);

    setProyectos(data);
    setTotal(data.length); // si backend devuelve total real, reemplazar
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, [page, rowsPerPage, sort]);

  // =============================
  // FILTRAR MANUALMENTE
  // =============================
  const handleFilter = () => {
    setPage(0);
    load();
    setOpenFilters(false);
  };

  const handleClear = () => {
    setNombre("");
    setEstado("");
    setSort("fecha_creacion:desc");
    setReparticionId("");
    setDireccionId("");
    setAreaId("");
    setDirecciones([]);
    setAreas([]);
    setPage(0);
    load();
  };

  // =============================
  // DELETE (PROTEGIDO)
  // =============================
  const handleDelete = async (id) => {
    if (!can("eliminar_proyectos")) {
      alert("No tenés permiso para eliminar proyectos.");
      return;
    }

    if (!window.confirm("¿Eliminar proyecto?")) return;

    await deleteProyecto(id);
    load();
  };

  // =============================
  // LOADING UI
  // =============================
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
  //  RENDER PRINCIPAL
  // ============================================================
  return (
    <Box sx={{ p: 3 }}>

      {/* HEADER */}
      <Stack direction="row" justifyContent="space-between" mb={3}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Proyectos
        </Typography>

        <Stack direction="row" spacing={2}>
          <IconButton
            color="primary"
            onClick={() => setOpenFilters(true)}
            sx={{
              border: "1px solid",
              borderColor: "primary.main",
              borderRadius: 2,
            }}
          >
            <FilterListIcon />
          </IconButton>

          {/* 🔥 BOTÓN CREAR PROTEGIDO */}
          {can("crear_proyectos") && (
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate("/proyectos/crear")}
            >
              Nuevo Proyecto
            </Button>
          )}
        </Stack>
      </Stack>

      {/* TABLA */}
      <Paper sx={{ borderRadius: 3, p: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>ID</strong></TableCell>
              <TableCell><strong>Nombre</strong></TableCell>
              <TableCell><strong>Objetivo</strong></TableCell>
              <TableCell><strong>Fecha creación</strong></TableCell>
              <TableCell align="right"><strong>Acciones</strong></TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {proyectos.map((p) => (
              <TableRow key={p.id} hover>
                <TableCell>{p.id}</TableCell>
                <TableCell>{p.nombre}</TableCell>
                <TableCell>{p.objetivo_general}</TableCell>
                <TableCell>{p.fecha_creacion?.substring(0, 10)}</TableCell>

                <TableCell align="right">
                  <Stack direction="row" spacing={1} justifyContent="flex-end">

                    {/* 🔥 VER */}
                    {can("ver_proyectos") && (
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<VisibilityIcon />}
                        onClick={() => navigate(`/proyectos/${p.id}`)}
                      >
                        Ver
                      </Button>
                    )}

                    {/* 🔥 EDITAR */}
                    {can("editar_proyectos") && (
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<EditIcon />}
                        onClick={() => navigate(`/proyectos/${p.id}/editar`)}
                      >
                        Editar
                      </Button>
                    )}

                    {/* 🔥 ELIMINAR */}
                    {can("eliminar_proyectos") && (
                      <Button
                        size="small"
                        color="error"
                        variant="outlined"
                        startIcon={<DeleteIcon />}
                        onClick={() => handleDelete(p.id)}
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
          count={total}
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

      {/* ============================================================ */}
      {/*  DRAWER LATERAL DE FILTROS INSTITUCIONALES PRO              */}
      {/* ============================================================ */}
      <Drawer
        anchor="right"
        open={openFilters}
        onClose={() => setOpenFilters(false)}
        sx={{
          "& .MuiDrawer-paper": {
            width: 320,
            p: 3,
            background: (theme) =>
              theme.palette.mode === "light"
                ? "rgba(255,255,255,0.85)"
                : "rgba(15,15,15,0.9)",
            backdropFilter: "blur(12px)",
          },
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Filtros
        </Typography>

        <Stack spacing={2}>

          {/* NOMBRE */}
          <TextField
            label="Buscar por nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            fullWidth
          />

          {/* ESTADO */}
          <TextField
            label="Estado"
            select
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            fullWidth
          >
            <MenuItem value="">Todos</MenuItem>
            <MenuItem value="activo">Activo</MenuItem>
            <MenuItem value="inactivo">Inactivo</MenuItem>
          </TextField>

          {/* ORDENAMIENTO */}
          <TextField
            label="Ordenar por"
            select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            fullWidth
          >
            <MenuItem value="fecha_creacion:desc">Fecha creación (desc)</MenuItem>
            <MenuItem value="fecha_creacion:asc">Fecha creación (asc)</MenuItem>
            <MenuItem value="nombre:asc">Nombre (A-Z)</MenuItem>
            <MenuItem value="nombre:desc">Nombre (Z-A)</MenuItem>
            <MenuItem value="version:desc">Versión (desc)</MenuItem>
            <MenuItem value="version:asc">Versión (asc)</MenuItem>
          </TextField>

          {/* REPARTICIÓN */}
          <TextField
            select
            label="Repartición"
            value={reparticionId}
            onChange={async (e) => {
              const val = e.target.value;
              setReparticionId(val);
              setDireccionId("");
              setAreaId("");
              await loadDirecciones(val);
              setAreas([]);
            }}
            fullWidth
          >
            <MenuItem value="">Todas</MenuItem>
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
            value={direccionId}
            onChange={async (e) => {
              const val = e.target.value;
              setDireccionId(val);
              setAreaId("");
              await loadAreas(val);
            }}
            fullWidth
            disabled={!reparticionId}
          >
            <MenuItem value="">Todas</MenuItem>
            {direcciones.map((d) => (
              <MenuItem key={d.id} value={d.id}>
                {d.nombre}
              </MenuItem>
            ))}
          </TextField>

          {/* ÁREA */}
          <TextField
            select
            label="Área"
            value={areaId}
            onChange={(e) => setAreaId(e.target.value)}
            fullWidth
            disabled={!direccionId}
          >
            <MenuItem value="">Todas</MenuItem>
            {areas.map((a) => (
              <MenuItem key={a.id} value={a.id}>
                {a.nombre}
              </MenuItem>
            ))}
          </TextField>

          {/* BOTONES */}
          <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
            <Button variant="contained" fullWidth onClick={handleFilter}>
              Aplicar
            </Button>

            <Button variant="outlined" fullWidth onClick={handleClear}>
              Limpiar
            </Button>
          </Stack>
        </Stack>
      </Drawer>
    </Box>
  );
};

export default ProjectList;
