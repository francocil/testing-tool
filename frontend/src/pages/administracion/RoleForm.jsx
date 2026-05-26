import { useState } from "react";
import { createRol, updateRol } from "../../api/roles";

export default function RoleForm({ role, onClose, onSaved }) {
    const [nombre, setNombre] = useState(role ? role.nombre : "");
    const [loading, setLoading] = useState(false);

    const isEdit = Boolean(role);

    // ------------------------------------------------------------
    // Guardar rol (crear o editar)
    // ------------------------------------------------------------
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            if (isEdit) {
                await updateRol(role.id, { nombre });
            } else {
                await createRol({ nombre });
            }

            onSaved(); // recarga lista en RolesPage
        } finally {
            setLoading(false);
        }
    };

    // ------------------------------------------------------------
    // Render
    // ------------------------------------------------------------
    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded shadow-lg w-96">
                <h2 className="text-xl font-bold mb-4">
                    {isEdit ? "Editar Rol" : "Nuevo Rol"}
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">
                            Nombre del Rol
                        </label>
                        <input
                            type="text"
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                            className="w-full border px-3 py-2 rounded"
                            required
                        />
                    </div>

                    <div className="flex justify-end space-x-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                        >
                            Cancelar
                        </button>

                        <button
                            type="submit"
                            disabled={loading}
                            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? "Guardando..." : "Guardar"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
