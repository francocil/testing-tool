import api from "./axiosClient";

export const getDirecciones = async (params = {}) => {
  const res = await api.get("/direcciones", { params });
  return res.data;
};
