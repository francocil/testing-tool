import { useEffect, useState } from "react";
import { getRoles } from "../../api/roles";
import {
    getRolesPorUsuario,
    asignarRolAUsuario,
    quitarRolDeUsuario
} from "../../api/usuarioRol";

export default function UsuarioRolEditor({ usuario, onClose }) {
    const [roles, setRoles] = useState([]);
    const [rolesUsuario, setRolesUsuario] = useState([]);
    const [loading, setLoading] = useState(true);

    // ------------------------------------------------------------
    // Cargar roles del sistema y roles del usuario
    // ------------------------------------------------------------
    const loadData = async () => {
        setLoading(true);
        try {
            const [allRoles, userRoles] = await Promise.all([
                getRoles(),
                getRolesPorUsuario(usuario.id)
            ]);

            setRoles(allRoles);
            setRolesUsuario(userRoles);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    // ------------------------------------------------------------
    // Verificar si el usuario tiene un rol
    // ------------------------------------------------------------
    const hasRole = (rolId) => {
        return rolesUsuario.some((r) => r.rol_id === rolId);
    };

    // ------------------------------------------------------------
    // Asignar o quitar rol
    // ------------------------------------------------------------
    const toggleRol = async (rol) => {
        const rolId = rol.id;

        // Si ya lo tiene → quitar
        if (hasRole(rolId)) {
            const ur = rolesUsuario.find((r) => r.rol_id === rolId);
            await quitarRolDeUsuario(ur.id);
        } else {
            await asignarRolAUsuario(usuario.id, rolId);
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
                    Roles del Usuario: {usuario.nombre}
                </h2>

                {loading ? (
                    <p>Cargando roles...</p>
                ) : (
                    <div className="space-y-2">
                        {roles.map((rol) => (
                            <label
                                key={rol.id}
                                className="flex items-center space-x-3 p-2 border rounded hover:bg-gray-50"
                            >
                                <input
                                    type="checkbox"
                                    checked={hasRole(rol.id)}
                                    onChange={() => toggleRol(rol)}
                                />
                                <span>{rol.nombre}</span>
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
