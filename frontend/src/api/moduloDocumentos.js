// ============================================================
// API - DOCUMENTOS DE MÓDULO
// ============================================================
//
// Backend espera:
// - modulo_id: Form
// - archivo: File
//
// ============================================================

import api from "./axiosClient";

// -----------------------------
// Listar documentos
// -----------------------------
export const getModuloDocumentos = async () => {
  const { data } = await api.get("/modulo-documentos");
  return data;
};

// -----------------------------
// Obtener documento
// -----------------------------
export const getModuloDocumento = async (id) => {
  const { data } = await api.get(`/modulo-documentos/${id}`);
  return data;
};

// -----------------------------
// Subir documento
// -----------------------------
export const uploadModuloDocumento = async (moduloId, file) => {
  const formData = new FormData();
  formData.append("modulo_id", moduloId);
  formData.append("archivo", file);

  const { data } = await api.post("/modulo-documentos", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
};

// -----------------------------
// Actualizar documento
// -----------------------------
export const updateModuloDocumento = async (id, file = null) => {
  const formData = new FormData();

  if (file) {
    formData.append("archivo", file);
  }

  const { data } = await api.put(`/modulo-documentos/${id}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
};

// -----------------------------
// Eliminar documento
// -----------------------------
export const deleteModuloDocumento = async (id) => {
  await api.delete(`/modulo-documentos/${id}`);
};

// -----------------------------
// Descargar / abrir documento
// -----------------------------
export const downloadModuloDocumento = async (id, filename) => {
  const response = await api.get(`/modulo-documentos/${id}`, {
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
