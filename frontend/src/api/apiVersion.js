import axiosClient from "./axiosClient";

export const getVersiones = (apiId) =>
  axiosClient.get(`/apis/versiones/by-api/${apiId}`);

export const getVersion = (versionId) =>
  axiosClient.get(`/apis/versiones/${versionId}`);

export const crearVersionDesdeApi = (apiId) =>
  axiosClient.post(`/apis/versiones/crear-desde-api/${apiId}`);
