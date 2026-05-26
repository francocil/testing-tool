import api from "./api";

// ------------------------------------------------------------
// ROLES — CRUD COMPLETO
// ------------------------------------------------------------

export async function getRoles() {
    const res = await api.get("/roles");
    return res.data;
}

export async function getRol(id) {
    const res = await api.get(`/roles/${id}`);
    return res.data;
}

export async function createRol(data) {
    const res = await api.post("/roles", data);
    return res.data;
}

export async function updateRol(id, data) {
    const res = await api.put(`/roles/${id}`, data);
    return res.data;
}

export async function deleteRol(id) {
    await api.delete(`/roles/${id}`);
}
