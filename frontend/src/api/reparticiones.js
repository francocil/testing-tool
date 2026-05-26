import api from "./axiosClient";

export const getReparticiones = async () => {
  const res = await api.get("/reparticiones");
  return res.data;
};
