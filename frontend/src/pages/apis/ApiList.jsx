import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../api/axiosClient";

export default function ApiList() {
  const navigate = useNavigate();
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);

  const cargarApis = async () => {
    try {
      const res = await axios.get("/apis");
      setApis(res.data);
    } catch (err) {
      console.error("Error cargando APIs", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    cargarApis();
  }, []);

  if (loading) return <p>Cargando APIs...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>APIs registradas</h1>

      <button onClick={() => navigate("/apis/nueva")}>Crear API</button>

      <table border="1" cellPadding="8" style={{ width: "100%", marginTop: "20px" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Método</th>
            <th>Endpoint</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {apis.map((api) => (
            <tr key={api.id}>
              <td>{api.id}</td>
              <td>{api.nombre}</td>
              <td>{api.metodo}</td>
              <td>{api.endpoint}</td>
              <td>
                <button onClick={() => navigate(`/apis/${api.id}`)}>Ver</button>
                <button onClick={() => navigate(`/apis/${api.id}/editar`)}>Editar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
