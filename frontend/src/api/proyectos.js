// ============================================================
//  API - PROYECTOS
// ============================================================
//
// Wrapper de llamadas HTTP al backend para el recurso "proyectos".
// Usa la instancia axiosClient (api) con JWT ya configurado.
//
// Endpoints backend:
//   GET    /proyectos
//   GET    /proyectos/{id}
//   POST   /proyectos
//   PUT    /proyectos/{id}
//   DELETE /proyectos/{id}
//
// ============================================================

import api from "./axiosClient";

// ============================================================
//  LISTAR PROYECTOS (con filtros, paginación y ordenamiento)
// ============================================================
export const getProyectos = async (params = {}) => {
  const { data } = await api.get("/proyectos", { params });
  return data;
};

export const getProyecto = async (id) => {
  const { data } = await api.get(`/proyectos/${id}`);
  return data;
};

export const createProyecto = async (payload) => {
  const { data } = await api.post("/proyectos", payload);
  return data;
};

export const updateProyecto = async (id, payload) => {
  const { data } = await api.put(`/proyectos/${id}`, payload);
  return data;
};

export const deleteProyecto = async (id) => {
  await api.delete(`/proyectos/${id}`);
};
