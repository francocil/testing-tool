// ============================================================
// API - CASOS DE PRUEBA
// ============================================================
//
// Endpoints backend:
// GET    /casos-prueba/modulo/{modulo_id}
// GET    /casos-prueba/{id}
// POST   /casos-prueba
// PUT    /casos-prueba/{id}
// DELETE /casos-prueba/{id}
//
// ============================================================

import api from "./axiosClient";

// ------------------------------------------------------------
// Listar casos de un módulo específico
// ------------------------------------------------------------
export const getCasosPorModulo = async (moduloId) => {
  const { data } = await api.get(`/casos-prueba/modulo/${moduloId}`);
  return data;
};

// ------------------------------------------------------------
// Obtener un caso por ID
// ------------------------------------------------------------
export const getCasoPrueba = async (id) => {
  const { data } = await api.get(`/casos-prueba/${id}`);
  return data;
};

// ------------------------------------------------------------
// Crear un nuevo caso de prueba
// ------------------------------------------------------------
export const createCasoPrueba = async (payload) => {
  const { data } = await api.post("/casos-prueba", payload);
  return data;
};

// ------------------------------------------------------------
// Actualizar un caso de prueba existente
// ------------------------------------------------------------
export const updateCasoPrueba = async (id, payload) => {
  const { data } = await api.put(`/casos-prueba/${id}`, payload);
  return data;
};

// ------------------------------------------------------------
// Eliminar un caso de prueba
// ------------------------------------------------------------
export const deleteCasoPrueba = async (id) => {
  await api.delete(`/casos-prueba/${id}`);
};
