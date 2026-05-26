import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "../../api/axiosClient";

export default function ApiForm() {
  const { apiId } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    nombre: "",
    descripcion: "",
    metodo: "GET",
    base_url: "",
    endpoint: "",
    auth_tipo: "",
    auth_config: {},
    headers_por_defecto: {},
    body_ejemplo: {},
    timeout_segundos: 30,
    retries: 0,
  });

  const [loading, setLoading] = useState(false);

  const loadApi = async () => {
    try {
      const res = await axios.get(`/apis/${apiId}`);
      setForm(res.data);
    } catch (err) {
      console.error("Error cargando API", err);
    }
  };

  useEffect(() => {
    if (apiId) loadApi();
  }, [apiId]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const guardar = async () => {
    setLoading(true);

    try {
      if (apiId) {
        await axios.put(`/apis/${apiId}`, form);
      } else {
        await axios.post("/apis", form);
      }

      navigate("/apis");
    } catch (err) {
      console.error("Error guardando API", err);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>{apiId ? "Editar API" : "Crear API"}</h1>

      <input
        type="text"
        name="nombre"
        placeholder="Nombre"
        value={form.nombre}
        onChange={handleChange}
      />

      <textarea
        name="descripcion"
        placeholder="Descripción"
        value={form.descripcion}
        onChange={handleChange}
      />

      <select name="metodo" value={form.metodo} onChange={handleChange}>
        <option>GET</option>
        <option>POST</option>
        <option>PUT</option>
        <option>DELETE</option>
      </select>

      <input
        type="text"
        name="base_url"
        placeholder="Base URL"
        value={form.base_url}
        onChange={handleChange}
      />

      <input
        type="text"
        name="endpoint"
        placeholder="/endpoint"
        value={form.endpoint}
        onChange={handleChange}
      />

      <button onClick={guardar} disabled={loading}>
        {loading ? "Guardando..." : "Guardar"}
      </button>
    </div>
  );
}
