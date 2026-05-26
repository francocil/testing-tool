// ============================================================
// API - DOCUMENTOS DE PROYECTO (CORREGIDO)
// ============================================================

import api from "./axiosClient";

// -----------------------------
// Listar documentos
// -----------------------------
export const getProyectoDocumentos = async () => {
  const { data } = await api.get("/proyecto-documentos");
  return data;
};

// -----------------------------
// Subir documento
// -----------------------------
export const uploadProyectoDocumento = async (proyectoId, file, descripcion = "") => {
  const formData = new FormData();
  formData.append("proyecto_id", proyectoId);
  formData.append("archivo", file);
  formData.append("descripcion", descripcion);

  const { data } = await api.post("/proyecto-documentos", formData); // ✔ SIN HEADERS
  
  return data;
};

// -----------------------------
// Eliminar documento
// -----------------------------
export const deleteProyectoDocumento = async (id) => {
  await api.delete(`/proyecto-documentos/${id}`);
};

// -----------------------------
// Descargar / abrir documento (CORREGIDO)
// -----------------------------
export const downloadProyectoDocumento = async (id) => {
  const response = await api.get(`/proyecto-documentos/${id}`, {
    responseType: "blob",
  });

  const blob = response.data;
  const fileURL = URL.createObjectURL(blob);

  // Intentar obtener nombre desde Content-Disposition
  let filename = "archivo";

  const disposition = response.headers["content-disposition"];
  if (disposition) {
    const match = disposition.match(/filename="?([^"]+)"?/);
    if (match && match[1]) {
      filename = match[1];
    }
  }

  // Detectar tipo MIME
  const mime = blob.type;

  // Si es PDF o imagen → abrir en nueva pestaña
  if (mime.includes("pdf") || mime.includes("image/")) {
    window.open(fileURL, "_blank");
    return;
  }

  // Si es otro tipo → descargar
  const link = document.createElement("a");
  link.href = fileURL;
  link.download = filename;
  link.click();
};
