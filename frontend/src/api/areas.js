import api from "./axiosClient";

export const getAreas = async (params = {}) => {
  const res = await api.get("/areas", { params });
  return res.data;
};
