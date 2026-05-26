// Obtener el usuario autenticado.
// Usa el token automáticamente porque axiosClient ya lo agrega en headers.
import axiosClient from "./axiosClient";

export const loginRequest = async (email, password) => {
  const response = await axiosClient.post("/auth/login", {
    email,
    password,
  });

  return response.data;
};

export const getCurrentUser = async () => {
  const response = await axiosClient.get("/auth/me");
  return response.data;
};
