// ============================================================
// API - DOCUMENTOS DE PASO (CORREGIDO)
// ============================================================

import api from "./axiosClient";

// -----------------------------
// Listar documentos por paso
// -----------------------------
export const getDocumentosByPaso = async (pasoId) => {
  const { data } = await api.get(`/pasos-documentos?paso_id=${pasoId}`);
  return data;
};

// -----------------------------
// Obtener documento
// -----------------------------
export const getPasoDocumento = async (id) => {
  const { data } = await api.get(`/pasos-documentos/${id}`);
  return data;
};

// -----------------------------
// Subir documento
// -----------------------------
export const uploadPasoDocumento = async (pasoId, file) => {
  const formData = new FormData();
  formData.append("paso_id", pasoId);
  formData.append("archivo", file);

  const { data } = await api.post("/pasos-documentos", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
};

// -----------------------------
// Actualizar documento
// -----------------------------
export const updatePasoDocumento = async (id, file = null) => {
  const formData = new FormData();

  if (file) {
    formData.append("archivo", file);
  }

  const { data } = await api.put(`/pasos-documentos/${id}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
};

// -----------------------------
// Eliminar documento
// -----------------------------
export const deletePasoDocumento = async (id) => {
  await api.delete(`/pasos-documentos/${id}`);
};

// -----------------------------
// Descargar / abrir documento
// -----------------------------
export const downloadPasoDocumento = async (id, filename) => {
  const response = await api.get(`/pasos-documentos/${id}`, {
    responseType: "blob",
  });

  const blob = response.data;
  const fileURL = URL.createObjectURL(blob);

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
