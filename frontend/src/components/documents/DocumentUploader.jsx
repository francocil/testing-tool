// ============================================================
// COMPONENTE: DocumentUploader (CORREGIDO)
// ============================================================
//
// - Ahora envía pasoId + file correctamente
// - Limpia el input después de subir
// - Compatible con cualquier tipo de archivo
//
// ============================================================

import { useRef, useState } from "react";
import { Box, Button, Stack, Typography } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";

const DocumentUploader = ({ pasoId, onUpload, label = "Subir documento" }) => {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleSelectFile = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (!selectedFile) return;

    // 🔥 AHORA SÍ: enviamos pasoId + file
    onUpload(pasoId, selectedFile);

    // limpiar estado
    setSelectedFile(null);
    fileInputRef.current.value = "";
  };

  return (
    <Box>
      <Stack direction="row" spacing={2} alignItems="center">
        <Button
          variant="contained"
          startIcon={<UploadIcon />}
          onClick={handleSelectFile}
        >
          {label}
        </Button>

        {selectedFile && (
          <Typography variant="body2" color="text.secondary">
            {selectedFile.name}
          </Typography>
        )}

        {selectedFile && (
          <Button variant="outlined" onClick={handleUpload}>
            Confirmar
          </Button>
        )}
      </Stack>

      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
    </Box>
  );
};

export default DocumentUploader;
