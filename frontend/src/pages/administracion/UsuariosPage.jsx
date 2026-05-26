import { useEffect, useState } from "react";
import { getUsuarios, deleteUsuario } from "../../api/usuarios";
import UsuarioRolEditor from "./UsuarioRolEditor";

export default function UsuariosPage() {
    const [usuarios, setUsuarios] = useState([]);
    const [loading, setLoading] = useState(true);

    const [showRoleEditor, setShowRoleEditor] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);

    // ------------------------------------------------------------
    // Cargar usuarios
    // ------------------------------------------------------------
    const loadUsuarios = async () => {
        setLoading(true);
        try {
            const data = await getUsuarios();
            setUsuarios(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadUsuarios();
    }, []);

    // ------------------------------------------------------------
    // Eliminar usuario
    // ------------------------------------------------------------
    const handleDelete = async (id) => {
        if (!confirm("¿Eliminar este usuario?")) return;
        await deleteUsuario(id);
        loadUsuarios();
    };

    // ------------------------------------------------------------
    // Abrir editor de roles
    // ------------------------------------------------------------
    const handleRoles = (usuario) => {
        setSelectedUser(usuario);
        setShowRoleEditor(true);
    };

    // ------------------------------------------------------------
    // Render
    // ------------------------------------------------------------
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Administración de Usuarios</h1>

            {loading ? (
                <p>Cargando usuarios...</p>
            ) : (
                <table className="w-full border-collapse">
                    <thead>
                        <tr className="bg-gray-100 text-left">
                            <th className="p-2 border">ID</th>
                            <th className="p-2 border">Nombre</th>
                            <th className="p-2 border">Email</th>
                            <th className="p-2 border">Activo</th>
                            <th className="p-2 border">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {usuarios.map((u) => (
                            <tr key={u.id} className="hover:bg-gray-50">
                                <td className="p-2 border">{u.id}</td>
                                <td className="p-2 border">{u.nombre}</td>
                                <td className="p-2 border">{u.email}</td>
                                <td className="p-2 border">
                                    {u.activo ? "Sí" : "No"}
                                </td>
                                <td className="p-2 border space-x-2">
                                    <button
                                        onClick={() => handleRoles(u)}
                                        className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                                    >
                                        Roles
                                    </button>

                                    <button
                                        onClick={() => handleDelete(u.id)}
                                        className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                                    >
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {/* Modal Editor de Roles */}
            {showRoleEditor && (
                <UsuarioRolEditor
                    usuario={selectedUser}
                    onClose={() => setShowRoleEditor(false)}
                />
            )}
        </div>
    );
}
