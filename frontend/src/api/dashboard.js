// ============================================================
//  DASHBOARD API CLIENT
// ============================================================
//
// Este módulo centraliza las llamadas a la API necesarias para
// obtener los datos del Dashboard:
//
// - Proyectos
// - Casos de Prueba
// - Ejecuciones
//
// Todas las funciones utilizan axiosClient, que ya incluye:
// - BaseURL configurada
// - Token JWT automáticamente en cada request
//
// ============================================================

import axiosClient from "./axiosClient";

/**
 * Obtiene la lista completa de proyectos.
 * Endpoint backend: GET /proyectos
 *
 * @returns {Promise<Array>} Lista de proyectos
 */
export const fetchProyectos = async () => {
  const response = await axiosClient.get("/proyectos");
  return response.data;
};

/**
 * Obtiene todos los casos de prueba del sistema.
 * Endpoint backend: GET /casos-prueba
 *
 * @returns {Promise<Array>} Lista de casos de prueba
 */
export const fetchCasosPrueba = async () => {
  const response = await axiosClient.get("/casos-prueba");
  return response.data;
};

/**
 * Obtiene todas las ejecuciones registradas.
 * Endpoint backend: GET /ejecuciones
 *
 * @returns {Promise<Array>} Lista de ejecuciones
 */
export const fetchEjecuciones = async () => {
  const response = await axiosClient.get("/ejecuciones");
  return response.data;
};
