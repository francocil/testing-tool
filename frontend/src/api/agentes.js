import api from "./axiosClient";

export const getAgentes = async () => {
  const res = await api.get("/agentes");
  return res.data;
};

export const createAgente = async (data) => {
  const res = await api.post("/agentes", data);
  return res.data;
};

export const updateAgente = async (id, data) => {
  const res = await api.put(`/agentes/${id}`, data);
  return res.data;
};

export const deleteAgente = async (id) => {
  const res = await api.delete(`/agentes/${id}`);
  return res.data;
};

// ⭐ NUEVO: obtener agente por ID (para el modal de detalle)
export const obtenerAgente = async (id) => {
  const res = await api.get(`/agentes/${id}`);
  return res.data;
};
