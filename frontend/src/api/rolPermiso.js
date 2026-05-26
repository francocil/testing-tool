import api from "./api";

// ------------------------------------------------------------
// ASIGNACIÓN DE PERMISOS A ROLES
// ------------------------------------------------------------

export async function getPermisosPorRol(rolId) {
    const res = await api.get(`/rol-permiso/rol/${rolId}`);
    return res.data;
}

export async function asignarPermisoARol(rolId, permisoId) {
    const res = await api.post("/rol-permiso", {
        rol_id: rolId,
        permiso_id: permisoId
    });
    return res.data;
}

export async function quitarPermisoDeRol(rolPermisoId) {
    await api.delete(`/rol-permiso/${rolPermisoId}`);
}
