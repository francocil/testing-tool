// ============================================================
//  API - MÓDULOS
// ============================================================
//
// Endpoints backend:
//   GET    /modulos/proyecto/{proyecto_id}
//   GET    /modulos/{id}
//   POST   /modulos
//   PUT    /modulos/{id}
//   DELETE /modulos/{id}
//
// ============================================================

import api from "./axiosClient";

export const getModulosPorProyecto = async (proyectoId) => {
  const { data } = await api.get(`/modulos/proyecto/${proyectoId}`);
  return data;
};

export const getModulo = async (id) => {
  const { data } = await api.get(`/modulos/${id}`);
  return data;
};

export const createModulo = async (payload) => {
  const { data } = await api.post("/modulos", payload);
  return data;
};

export const updateModulo = async (id, payload) => {
  const { data } = await api.put(`/modulos/${id}`, payload);
  return data;
};

export const deleteModulo = async (id) => {
  await api.delete(`/modulos/${id}`);
};
