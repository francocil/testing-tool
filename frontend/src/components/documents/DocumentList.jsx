// ============================================================
// COMPONENTE: DocumentList
// ------------------------------------------------------------
// Lista de documentos asociados a un paso.
// Incluye acciones de descarga y eliminación.
//
// 🔥 NOTA IMPORTANTE:
// El botón de descarga usa <button> HTML puro para evitar que
// React Router intercepte el click dentro del modal StepDetail.
// ============================================================

import {
  Box,
  Paper,
  Stack,
  Typography,
  IconButton,
  Tooltip,
} from "@mui/material";

import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";

const DocumentList = ({ documents = [], onDownload, onDelete }) => {
  if (!documents.length) {
    return (
      <Box sx={{ py: 2 }}>
        <Typography variant="body2" color="text.secondary">
          No hay documentos cargados.
        </Typography>
      </Box>
    );
  }

  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        borderRadius: 3,
        background: (theme) =>
          theme.palette.mode === "light"
            ? "rgba(255,255,255,0.8)"
            : "rgba(20,20,20,0.9)",
      }}
    >
      <Stack spacing={2}>
        {documents.map((doc) => {
          // Extraer nombre del archivo desde archivo_url
          const nombreArchivo = doc.archivo_url?.split(/[\\/]/).pop();

          return (
            <Stack
              key={doc.id}
              direction="row"
              justifyContent="space-between"
              alignItems="center"
              sx={{
                p: 1.5,
                borderRadius: 2,
                background: (theme) =>
                  theme.palette.mode === "light"
                    ? "rgba(255,255,255,0.6)"
                    : "rgba(40,40,40,0.9)",
              }}
            >
              {/* Información del documento */}
              <Box>
                <Typography sx={{ fontWeight: 600 }}>
                  {nombreArchivo}
                </Typography>

                {doc.descripcion && (
                  <Typography variant="body2" color="text.secondary">
                    {doc.descripcion}
                  </Typography>
                )}

                <Typography variant="caption" color="text.secondary">
                  {doc.fecha_subida
                    ? new Date(doc.fecha_subida).toLocaleString()
                    : ""}
                </Typography>
              </Box>

              {/* Acciones */}
              <Stack direction="row" spacing={1}>

                {/* Descargar */}
                <Tooltip title="Abrir / Descargar">
                  <button
                    type="button"
                    onClick={() => onDownload(doc.id, nombreArchivo)}
                    style={{
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      padding: 6,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <DownloadIcon />
                  </button>
                </Tooltip>

                {/* Eliminar */}
                <Tooltip title="Eliminar documento">
                  <IconButton
                    color="error"
                    onClick={() => onDelete(doc.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>

              </Stack>
            </Stack>
          );
        })}
      </Stack>
    </Paper>
  );
};

export default DocumentList;
