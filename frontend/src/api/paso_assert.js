import api from "./axiosClient";

// ------------------------------------------------------------
// Listar asserts por paso
// ------------------------------------------------------------
export const getAssertsByPaso = async (pasoId) => {
  const res = await api.get(`/paso-assert/by-paso/${pasoId}`);
  return res.data;
};

// ------------------------------------------------------------
// Crear assert
// ------------------------------------------------------------
export const createAssert = async (data) => {
  const res = await api.post(`/paso-assert/`, data);
  return res.data;
};

// ------------------------------------------------------------
// Actualizar assert
// ------------------------------------------------------------
export const updateAssert = async (id, data) => {
  const res = await api.put(`/paso-assert/${id}`, data);
  return res.data;
};

// ------------------------------------------------------------
// Eliminar assert
// ------------------------------------------------------------
export const deleteAssert = async (id) => {
  await api.delete(`/paso-assert/${id}`);
};
