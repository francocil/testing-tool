import { useEffect, useState } from "react";
import { getPermisos } from "../../api/permisos";
import {
    getPermisosPorRol,
    asignarPermisoARol,
    quitarPermisoDeRol
} from "../../api/rolPermiso";

export default function RolePermissionEditor({ role, onClose }) {
    const [permisos, setPermisos] = useState([]);
    const [permisosRol, setPermisosRol] = useState([]);
    const [loading, setLoading] = useState(true);

    // ------------------------------------------------------------
    // Cargar permisos del sistema y permisos del rol
    // ------------------------------------------------------------
    const loadData = async () => {
        setLoading(true);
        try {
            const [allPerms, rolePerms] = await Promise.all([
                getPermisos(),
                getPermisosPorRol(role.id)
            ]);

            setPermisos(allPerms);
            setPermisosRol(rolePerms);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    // ------------------------------------------------------------
    // Verificar si el rol tiene un permiso
    // ------------------------------------------------------------
    const hasPerm = (permisoId) => {
        return permisosRol.some((p) => p.permiso_id === permisoId);
    };

    // ------------------------------------------------------------
    // Asignar o quitar permiso
    // ------------------------------------------------------------
    const togglePermiso = async (permiso) => {
        const permisoId = permiso.id;

        // Si ya lo tiene → quitar
        if (hasPerm(permisoId)) {
            const rp = permisosRol.find((p) => p.permiso_id === permisoId);
            await quitarPermisoDeRol(rp.id);
        } else {
            await asignarPermisoARol(role.id, permisoId);
        }

        loadData();
    };

    // ------------------------------------------------------------
    // Render
    // ------------------------------------------------------------
    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded shadow-lg w-[600px] max-h-[80vh] overflow-y-auto">
                <h2 className="text-xl font-bold mb-4">
                    Permisos del Rol: {role.nombre}
                </h2>

                {loading ? (
                    <p>Cargando permisos...</p>
                ) : (
                    <div className="space-y-2">
                        {permisos.map((permiso) => (
                            <label
                                key={permiso.id}
                                className="flex items-center space-x-3 p-2 border rounded hover:bg-gray-50"
                            >
                                <input
                                    type="checkbox"
                                    checked={hasPerm(permiso.id)}
                                    onChange={() => togglePermiso(permiso)}
                                />
                                <span>{permiso.nombre}</span>
                            </label>
                        ))}
                    </div>
                )}

                <div className="flex justify-end mt-4">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                    >
                        Cerrar
                    </button>
                </div>
            </div>
        </div>
    );
}
