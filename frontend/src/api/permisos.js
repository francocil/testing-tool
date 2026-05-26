import api from "./api"; // tu instancia axios

// ------------------------------------------------------------
// PERMISOS — CRUD BÁSICO
// ------------------------------------------------------------

export async function getPermisos() {
    const res = await api.get("/permisos");
    return res.data;
}
