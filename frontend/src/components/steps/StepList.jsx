// ============================================================
// StepList.jsx (VERSIÓN PRO INSTITUCIONAL)
// Grilla completa con filtros + paginación + acciones celestes
// ============================================================

import { useState, useMemo } from "react";
import {
  Box,
  Paper,
  Stack,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TablePagination,
  TextField,
  MenuItem,
  Button,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import FlagIcon from "@mui/icons-material/Flag"; // Ícono institucional

const StepList = ({ pasos, onView, onEdit, onDelete }) => {
  // =============================
  // PAGINACIÓN PRO
  // =============================
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // =============================
  // FILTROS PRO
  // =============================
  const [filtros, setFiltros] = useState({
    texto: "",
    tipo: "",
    estado: "",
  });

  const tiposUnicos = [...new Set(pasos.map((p) => p.tipo).filter(Boolean))];
  const estadosUnicos = [...new Set(pasos.map((p) => p.estado).filter(Boolean))];

  // =============================
  // FILTRADO PRO
  // =============================
  const pasosFiltrados = useMemo(() => {
    const t = filtros.texto.toLowerCase();

    return pasos.filter((p) => {
      return (
        (!t ||
          p.nombre.toLowerCase().includes(t) ||
          p.descripcion?.toLowerCase().includes(t)) &&
        (!filtros.tipo || p.tipo === filtros.tipo) &&
        (!filtros.estado || p.estado === filtros.estado)
      );
    });
  }, [pasos, filtros]);

  // =============================
  // PAGINACIÓN PRO
  // =============================
  const paginated = useMemo(() => {
    const start = page * rowsPerPage;
    return pasosFiltrados.slice(start, start + rowsPerPage);
  }, [pasosFiltrados, page, rowsPerPage]);

  // =============================
  // UI
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
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Pasos del Caso
        </Typography>
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

          {/* TIPO */}
          <TextField
            select
            label="Tipo"
            value={filtros.tipo}
            onChange={(e) =>
              setFiltros({ ...filtros, tipo: e.target.value })
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">Todos</MenuItem>
            {tiposUnicos.map((t) => (
              <MenuItem key={t} value={t}>
                {t}
              </MenuItem>
            ))}
          </TextField>

          {/* ESTADO */}
          <TextField
            select
            label="Estado"
            value={filtros.estado}
            onChange={(e) =>
              setFiltros({ ...filtros, estado: e.target.value })
            }
            sx={{ minWidth: 180 }}
          >
            <MenuItem value="">Todos</MenuItem>
            {estadosUnicos.map((e) => (
              <MenuItem key={e} value={e}>
                {e}
              </MenuItem>
            ))}
          </TextField>
        </Stack>
      </Box>

      {/* TABLA */}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell width={40}></TableCell>
            <TableCell>Orden</TableCell>
            <TableCell>Nombre</TableCell>
            <TableCell>Descripción</TableCell>
            <TableCell>Tipo</TableCell>
            <TableCell>Estado</TableCell>
            <TableCell align="right">Acciones</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {paginated.map((p) => (
            <TableRow
              key={p.id}
              hover
              sx={{ cursor: "pointer" }}
              onClick={() => onView(p)}
            >
              <TableCell>
                <FlagIcon color="primary" />
              </TableCell>

              <TableCell>{p.orden}</TableCell>
              <TableCell>{p.nombre}</TableCell>
              <TableCell>{p.descripcion}</TableCell>
              <TableCell>{p.tipo}</TableCell>
              <TableCell>{p.estado}</TableCell>

              <TableCell align="right">
                <Button
                  size="small"
                  variant="contained"
                  color="primary"
                  startIcon={<VisibilityIcon />}
                  onClick={(e) => {
                    e.stopPropagation();
                    onView(p);
                  }}
                  sx={{ mr: 1 }}
                >
                  Ver
                </Button>

                <Button
                  size="small"
                  variant="contained"
                  color="primary"
                  startIcon={<EditIcon />}
                  onClick={(e) => {
                    e.stopPropagation();
                    onEdit(p);
                  }}
                  sx={{ mr: 1 }}
                >
                  Editar
                </Button>

                <Button
                  size="small"
                  color="error"
                  variant="contained"
                  startIcon={<DeleteIcon />}
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(p.id);
                  }}
                >
                  Eliminar
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* PAGINACIÓN PRO */}
      <TablePagination
        component="div"
        count={pasosFiltrados.length}
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

export default StepList;
