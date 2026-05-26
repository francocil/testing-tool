import api from "./axiosClient";

export const updateParametro = async (id, data) => {
  const res = await api.put(`/objetos-parametros/${id}/valor`, data);
  return res.data;
};
