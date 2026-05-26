import api from "./axiosClient";

// Listar pasos de un caso
export const getPasosByCaso = async (casoId) => {
  const response = await api.get(`/pasos/?caso_id=${casoId}`);
  return response.data;
};

// Obtener paso por ID
export const getPaso = async (id) => {
  const response = await api.get(`/pasos/${id}`);
  return response.data;
};

// Crear paso
export const createPaso = async (data) => {
  const response = await api.post("/pasos/", data);
  return response.data;
};

// Actualizar paso
export const updatePaso = async (id, data) => {
  const response = await api.put(`/pasos/${id}`, data);
  return response.data;
};

// Eliminar paso
export const deletePaso = async (id) => {
  await api.delete(`/pasos/${id}`);
};
