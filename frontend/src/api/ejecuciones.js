// ============================================================
// API: EJECUCIONES (CREADO PARA EL MOTOR REAL)
// ============================================================

import api from "./axiosClient";

// ------------------------------------------------------------
// Crear ejecución del caso
// ------------------------------------------------------------
export const crearEjecucion = async ({ caso_id, modo, usuario_id }) => {
  const res = await api.post("/ejecuciones/", {
    caso_id,
    modo,
    usuario_id,   // ✔ AHORA SÍ EXISTE
  });
  return res.data;
};

// ------------------------------------------------------------
// Obtener ejecución por ID
// ------------------------------------------------------------
export const getEjecucion = async (ejecucionId) => {
  const { data } = await api.get(`/ejecuciones/${ejecucionId}`);
  return data;
};

// ------------------------------------------------------------
// Obtener pasos ejecutados dentro de una ejecución
// ------------------------------------------------------------
export const getEjecucionPasos = async (ejecucionId) => {
  const { data } = await api.get(
    `/ejecuciones-pasos/ejecucion/${ejecucionId}`
  );
  return data;
};

// ------------------------------------------------------------
// Ejecutar ejecución completa (modo automático)
// ------------------------------------------------------------
export const ejecutarEjecucion = async (ejecucionId) => {
  const { data } = await api.post(
    `/ejecuciones/${ejecucionId}/ejecutar`
  );
  return data;
};

// ------------------------------------------------------------
// Ejecutar solo el siguiente paso (modo paso a paso)
// ------------------------------------------------------------
export const ejecutarSiguientePaso = async (ejecucionId) => {
  const { data } = await api.post(
    `/ejecuciones/${ejecucionId}/siguiente-paso`
  );
  return data;
};

// ------------------------------------------------------------
// Registrar paso manual
// ------------------------------------------------------------
export const registrarPasoManual = async (
  ejecucionId,
  pasoId,
  estado,
  resultado
) => {
  const { data } = await api.post(
    `/ejecuciones/${ejecucionId}/pasos/${pasoId}/manual`,
    { estado, resultado }
  );
  return data;
};
