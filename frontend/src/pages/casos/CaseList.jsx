// ============================================================
// LISTADO DE CASOS DE PRUEBA POR MÓDULO (CORREGIDO + DOCUMENTADO)
// ============================================================
//
// - Se usa en ModuleDetail.jsx
// - Lista todos los casos del módulo actual
// - Permite ver, editar y eliminar
// - Navegación correcta hacia CasoDetail.jsx
//
// ============================================================

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Paper,
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Stack,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { getCasosPorModulo, deleteCasoPrueba } from "../../api/casosPrueba";

const CaseList = () => {
  const { id, moduloId } = useParams(); // ← Proyecto + Módulo
  const navigate = useNavigate();

  const [casos, setCasos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ------------------------------------------------------------
  // Cargar casos del módulo
  // ------------------------------------------------------------
  const loadCasos = async () => {
    try {
      setLoading(true);
      const data = await getCasosPorModulo(moduloId);
      setCasos(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("No se pudieron cargar los casos de prueba.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCasos();
  }, [moduloId]);

  // ------------------------------------------------------------
  // Navegación
  // ------------------------------------------------------------
  const handleCreate = () => {
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos/crear`);
  };

  const handleView = (casoId) => {
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos/${casoId}`);
  };

  const handleEdit = (casoId) => {
    navigate(`/proyectos/${id}/modulos/${moduloId}/casos/${casoId}/editar`);
  };

  const handleDelete = async (casoId) => {
    if (!window.confirm("¿Seguro que deseas eliminar este caso de prueba?")) return;

    try {
      await deleteCasoPrueba(casoId);
      await loadCasos();
    } catch (err) {
      console.error(err);
      alert("No se pudo eliminar el caso de prueba.");
    }
  };

  // ------------------------------------------------------------
  // Estados de carga / error
  // ------------------------------------------------------------
  if (loading) {
    return (
      <Box sx={{ mt: 2 }}>
        <Typography>Cargando casos de prueba...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  // ------------------------------------------------------------
  // Render principal
  // ------------------------------------------------------------
  return (
    <Paper
      elevation={3}
      sx={{
        p: 2,
        borderRadius: 3,
        background: (theme) =>
          theme.palette.mode === "light"
            ? "rgba(255,255,255,0.85)"
            : "rgba(15,15,15,0.9)",
        backdropFilter: "blur(10px)",
      }}
    >
      {/* Encabezado */}
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 2 }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
          Casos de Prueba del Módulo
        </Typography>

        <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreate}>
          Nuevo Caso de Prueba
        </Button>
      </Stack>

      {/* Estado vacío */}
      {casos.length === 0 ? (
        <Box sx={{ py: 4, textAlign: "center" }}>
          <Typography variant="body1" sx={{ mb: 1 }}>
            No hay casos de prueba cargados para este módulo.
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Creá el primer caso de prueba para comenzar a documentar y ejecutar pruebas.
          </Typography>
        </Box>
      ) : (
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Nombre</TableCell>
              <TableCell>Objetivo</TableCell>
              <TableCell>Versión actual</TableCell>
              <TableCell>Porcentaje aceptación</TableCell>
              <TableCell align="right">Acciones</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {casos.map((caso) => (
              <TableRow key={caso.id}>
                <TableCell>{caso.nombre}</TableCell>
                <TableCell>{caso.objetivo || "-"}</TableCell>

                <TableCell>{caso.version_actual ?? "-"}</TableCell>

                <TableCell>
                  {caso.porcentaje_aceptacion != null
                    ? `${caso.porcentaje_aceptacion}%`
                    : "-"}
                </TableCell>

                <TableCell align="right">
                  <Stack direction="row" spacing={1} justifyContent="flex-end">
                    <Button
                      size="small"
                      variant="text"
                      onClick={() => handleView(caso.id)}
                      startIcon={<VisibilityIcon />}
                    >
                      Ver
                    </Button>

                    <Button
                      size="small"
                      variant="text"
                      onClick={() => handleEdit(caso.id)}
                      startIcon={<EditIcon />}
                    >
                      Editar
                    </Button>

                    <Button
                      size="small"
                      color="error"
                      variant="text"
                      onClick={() => handleDelete(caso.id)}
                      startIcon={<DeleteIcon />}
                    >
                      Eliminar
                    </Button>
                  </Stack>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Paper>
  );
};

export default CaseList;
