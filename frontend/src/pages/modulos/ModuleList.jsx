// ============================================================
//  LISTADO DE MÓDULOS (CON PAGINACIÓN + FILTROS PRO)
// ============================================================
//
// - Lista módulos del proyecto
// - Botón “Crear Módulo”
// - Filtros por nombre, tipo_interfaz, tipo_gui
// - Paginación PRO
// - Diseño institucional glass
//
// ============================================================

import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
  Stack,
  TablePagination,
  TextField,
  MenuItem,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import LayersIcon from "@mui/icons-material/Layers";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";

import { getModulosPorProyecto, deleteModulo } from "../../api/modulos";
import useAuth from "/src/hooks/useAuth.js";

const ModuleList = ({ proyectoId }) => {
  const [modulos, setModulos] = useState([]);
  const [loading, setLoading] = useState(true);

  // PAGINACIÓN PRO
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // FILTROS PRO
  const [filtros, setFiltros] = useState({
    texto: "",
    tipo_interfaz: "",
    tipo_gui: "",
  });

  const navigate = useNavigate();
  const { role } = useAuth();
  const isAdmin = role?.toLowerCase() === "admin";

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await getModulosPorProyecto(proyectoId);
      setModulos(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [proyectoId]);

  const handleCreate = () => {
    navigate(`/proyectos/${proyectoId}/modulos/crear`);
  };

  const handleRowClick = (id) => {
    navigate(`/proyectos/${proyectoId}/modulos/${id}`);
  };

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (!isAdmin) return;

    const confirm = window.confirm("¿Eliminar módulo?");
    if (!confirm) return;

    await deleteModulo(id);
    await loadData();
  };

  // =============================
  // FILTRADO PRO
  // =============================
  const modulosFiltrados = useMemo(() => {
    return modulos.filter((m) => {
      const t = filtros.texto.toLowerCase();

      return (
        (!t ||
          m.nombre.toLowerCase().includes(t) ||
          m.tipo_interfaz.toLowerCase().includes(t) ||
          m.tipo_gui.toLowerCase().includes(t)) &&
        (!filtros.tipo_interfaz ||
          m.tipo_interfaz === filtros.tipo_interfaz) &&
        (!filtros.tipo_gui || m.tipo_gui === filtros.tipo_gui)
      );
    });
  }, [modulos, filtros]);

  // =============================
  // PAGINACIÓN PRO
  // =============================
  const paginated = useMemo(() => {
    const start = page * rowsPerPage;
    return modulosFiltrados.slice(start, start + rowsPerPage);
  }, [modulosFiltrados, page, rowsPerPage]);

  // =============================
  // LOADING
  // =============================
  if (loading) {
    return (
      <Stack direction="row" spacing={2} alignItems="center">
        <CircularProgress size={24} />
        <Typography>Cargando módulos...</Typography>
      </Stack>
    );
  }

  // =============================
  // ESTADO VACÍO
  // =============================
  if (!modulos.length) {
    return (
      <Box
        sx={{
          p: 3,
          borderRadius: 3,
          background: "rgba(0,123,255,0.08)",
          backdropFilter: "blur(12px)",
          textAlign: "center",
        }}
      >
        <WarningAmberIcon sx={{ fontSize: 40, mb: 1 }} color="primary" />
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          No hay módulos registrados
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Creá el primer módulo para este proyecto.
        </Typography>

        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          Crear Módulo
        </Button>
      </Box>
    );
  }

  // =============================
  // LISTADO CON FILTROS + PAGINACIÓN
  // =============================
  return (
    <Paper
      elevation={3}
      sx={{
        borderRadius: 3,
        overflow: "hidden",
        background: (theme) =>
          theme.palette.mode === "light"
            ? "rgba(255,255,255,0.8)"
            : "rgba(15,15,15,0.85)",
        backdropFilter: "blur(10px)",
      }}
    >
      {/* HEADER */}
      <Box sx={{ p: 2, display: "flex", justifyContent: "space-between" }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Módulos
        </Typography>

        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          Nuevo Módulo
        </Button>
      </Box>

      {/* FILTROS */}
      <Box sx={{ p: 2 }}>
        <Stack direction="row" spacing={2}>
          {/* TEXTO */}
          <TextField
            label="Buscar"
            fullWidth
            value={filtros.texto}
            onChange={(e) =>
              setFiltros({ ...filtros, texto: e.target.value })
            }
          />

          {/* TIPO INTERFAZ */}
          <TextField
            select
            label="Tipo Interfaz"
            value={filtros.tipo_interfaz}
            onChange={(e) =>
              setFiltros({ ...filtros, tipo_interfaz: e.target.value })
            }
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="">Todos</MenuItem>
            {[...new Set(modulos.map((m) => m.tipo_interfaz))].map((ti) => (
              <MenuItem key={ti} value={ti}>
                {ti}
              </MenuItem>
            ))}
          </TextField>

          {/* TIPO GUI */}
          <TextField
            select
            label="Tipo GUI"
            value={filtros.tipo_gui}
            onChange={(e) =>
              setFiltros({ ...filtros, tipo_gui: e.target.value })
            }
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="">Todos</MenuItem>
            {[...new Set(modulos.map((m) => m.tipo_gui))].map((tg) => (
              <MenuItem key={tg} value={tg}>
                {tg}
              </MenuItem>
            ))}
          </TextField>
        </Stack>
      </Box>

      {/* TABLA */}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Nombre</TableCell>
            <TableCell>Tipo Interfaz</TableCell>
            <TableCell>Tipo GUI</TableCell>
            <TableCell>Fecha creación</TableCell>
            {isAdmin && <TableCell align="right">Acciones</TableCell>}
          </TableRow>
        </TableHead>

        <TableBody>
          {paginated.map((m) => (
            <TableRow
              key={m.id}
              hover
              sx={{ cursor: "pointer" }}
              onClick={() => handleRowClick(m.id)}
            >
              <TableCell width={40}>
                <LayersIcon color="primary" />
              </TableCell>

              <TableCell>{m.nombre}</TableCell>
              <TableCell>{m.tipo_interfaz}</TableCell>
              <TableCell>{m.tipo_gui}</TableCell>
              <TableCell>
                {new Date(m.fecha_creacion).toLocaleString()}
              </TableCell>

              {isAdmin && (
                <TableCell align="right">
                  <Button
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/proyectos/${proyectoId}/modulos/${m.id}/editar`);
                    }}
                  >
                    Editar
                  </Button>

                  <Button
                    size="small"
                    color="error"
                    onClick={(e) => handleDelete(e, m.id)}
                  >
                    Eliminar
                  </Button>
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* PAGINACIÓN PRO */}
      <TablePagination
        component="div"
        count={modulosFiltrados.length}
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
  );
};

export default ModuleList;
