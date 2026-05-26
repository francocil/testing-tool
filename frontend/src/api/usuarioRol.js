import api from "./api";

// ------------------------------------------------------------
// ASIGNACIÓN DE ROLES A USUARIOS
// ------------------------------------------------------------

export async function getRolesPorUsuario(usuarioId) {
    const res = await api.get(`/usuario-rol/usuario/${usuarioId}`);
    return res.data;
}

export async function asignarRolAUsuario(usuarioId, rolId) {
    const res = await api.post("/usuario-rol", {
        usuario_id: usuarioId,
        rol_id: rolId
    });
    return res.data;
}

export async function quitarRolDeUsuario(usuarioRolId) {
    await api.delete(`/usuario-rol/${usuarioRolId}`);
}
