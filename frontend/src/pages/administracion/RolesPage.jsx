import { useEffect, useState } from "react";
import { getRoles, deleteRol } from "../../api/roles";
import RoleForm from "./RoleForm";
import RolePermissionEditor from "./RolePermissionEditor";
import usePermission from "../../hooks/usePermission";

export default function RolesPage() {
    // ============================================================
    // PERMISOS INSTITUCIONALES
    // ============================================================
    const { can } = usePermission();

    const puedeVer = can("seguridad_rol_ver");
    const puedeCrear = can("seguridad_rol_crear");
    const puedeEditar = can("seguridad_rol_editar");
    const puedeEliminar = can("seguridad_rol_eliminar");

    // Si NO puede ver, no mostramos nada
    if (!puedeVer) {
        return (
            <div className="p-6">
                <h2 className="text-xl text-red-600 font-semibold">
                    No tenés permisos para ver roles.
                </h2>
            </div>
        );
    }

    // ============================================================
    // ESTADOS
    // ============================================================
    const [roles, setRoles] = useState([]);
    const [loading, setLoading] = useState(true);

    const [showForm, setShowForm] = useState(false);
    const [editingRole, setEditingRole] = useState(null);

    const [showPermissionEditor, setShowPermissionEditor] = useState(false);
    const [selectedRole, setSelectedRole] = useState(null);

    // ============================================================
    // Cargar roles
    // ============================================================
    const loadRoles = async () => {
        setLoading(true);
        try {
            const data = await getRoles();
            setRoles(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadRoles();
    }, []);

    // ============================================================
    // Eliminar rol
    // ============================================================
    const handleDelete = async (id) => {
        if (!puedeEliminar) return;

        if (!confirm("¿Eliminar este rol?")) return;

        await deleteRol(id);
        loadRoles();
    };

    // ============================================================
    // Abrir formulario de creación
    // ============================================================
    const handleNew = () => {
        if (!puedeCrear) return;

        setEditingRole(null);
        setShowForm(true);
    };

    // ============================================================
    // Abrir formulario de edición
    // ============================================================
    const handleEdit = (role) => {
        if (!puedeEditar) return;

        setEditingRole(role);
        setShowForm(true);
    };

    // ============================================================
    // Abrir editor de permisos
    // ============================================================
    const handlePermissions = (role) => {
        if (!puedeEditar) return;

        setSelectedRole(role);
        setShowPermissionEditor(true);
    };

    // ============================================================
    // Render
    // ============================================================
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Administración de Roles</h1>

            <div className="mb-4">
                {puedeCrear && (
                    <button
                        onClick={handleNew}
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                        Nuevo Rol
                    </button>
                )}
            </div>

            {loading ? (
                <p>Cargando roles...</p>
            ) : (
                <table className="w-full border-collapse">
                    <thead>
                        <tr className="bg-gray-100 text-left">
                            <th className="p-2 border">ID</th>
                            <th className="p-2 border">Nombre</th>
                            <th className="p-2 border">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {roles.map((role) => (
                            <tr key={role.id} className="hover:bg-gray-50">
                                <td className="p-2 border">{role.id}</td>
                                <td className="p-2 border">{role.nombre}</td>
                                <td className="p-2 border space-x-2">
                                    {puedeEditar && (
                                        <button
                                            onClick={() => handleEdit(role)}
                                            className="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                                        >
                                            Editar
                                        </button>
                                    )}

                                    {puedeEditar && (
                                        <button
                                            onClick={() => handlePermissions(role)}
                                            className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                                        >
                                            Permisos
                                        </button>
                                    )}

                                    {puedeEliminar && (
                                        <button
                                            onClick={() => handleDelete(role.id)}
                                            className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                                        >
                                            Eliminar
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {/* Modal Formulario */}
            {showForm && (
                <RoleForm
                    role={editingRole}
                    onClose={() => setShowForm(false)}
                    onSaved={() => {
                        setShowForm(false);
                        loadRoles();
                    }}
                />
            )}

            {/* Modal Editor de Permisos */}
            {showPermissionEditor && (
                <RolePermissionEditor
                    role={selectedRole}
                    onClose={() => setShowPermissionEditor(false)}
                />
            )}
        </div>
    );
}
