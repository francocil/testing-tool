import { useEffect, useState } from "react";
import axios from "../../../api/axiosClient";

export default function ApiVersionList({ apiId }) {
  const [versiones, setVersiones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [detalle, setDetalle] = useState(null);
  const [error, setError] = useState("");

  const cargarVersiones = async () => {
    try {
      const res = await axios.get(`/apis/versiones/by-api/${apiId}`);
      setVersiones(res.data);
    } catch (err) {
      setError("Error cargando versiones");
    }
    setLoading(false);
  };

  useEffect(() => {
    cargarVersiones();
  }, [apiId]);

  const verDetalle = async (id) => {
    try {
      const res = await axios.get(`/apis/versiones/${id}`);
      setDetalle(res.data);
    } catch (err) {
      alert("Error cargando detalle");
    }
  };

  const crearVersion = async () => {
    try {
      await axios.post(`/apis/versiones/crear-desde-api/${apiId}`);
      await cargarVersiones();
    } catch (err) {
      alert("Error creando versión");
    }
  };

  const restaurar = async (id) => {
    if (!window.confirm("¿Seguro que querés restaurar esta versión?")) return;

    try {
      await axios.post(`/apis/versiones/rollback/${id}`);
      alert("Versión restaurada correctamente");
      await cargarVersiones();
    } catch (err) {
      alert("Error restaurando versión");
    }
  };

  const clonar = async (id) => {
    if (!window.confirm("¿Querés clonar esta versión como una nueva API?")) return;

    try {
      const res = await axios.post(`/apis/versiones/clonar/${id}`);
      const nuevaId = res.data.api_id;

      alert("API clonada correctamente");
      window.location.href = `/apis/${nuevaId}`;
    } catch (err) {
      alert("Error clonando versión");
    }
  };

  const exportar = async (id) => {
    try {
      const res = await axios.get(`/apis/versiones/exportar/${id}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `api_version_${id}.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Error exportando versión");
    }
  };

  if (loading) return <p>Cargando versiones...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Versiones de la API</h2>

      <button onClick={crearVersion} style={{ marginBottom: "10px" }}>
        Crear nueva versión
      </button>

      {versiones.length === 0 ? (
        <p>No hay versiones registradas.</p>
      ) : (
        <table border="1" cellPadding="8" style={{ width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Versión</th>
              <th>Método</th>
              <th>Endpoint</th>
              <th>Fecha</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {versiones.map((v) => (
              <tr key={v.id}>
                <td>{v.id}</td>
                <td>{v.version}</td>
                <td>{v.metodo}</td>
                <td>{v.endpoint}</td>
                <td>{v.fecha_creacion}</td>
                <td>
                  <button onClick={() => verDetalle(v.id)}>Ver</button>
                  <button style={{ marginLeft: "5px" }} onClick={() => restaurar(v.id)}>Restaurar</button>
                  <button style={{ marginLeft: "5px" }} onClick={() => clonar(v.id)}>Clonar</button>
                  <button style={{ marginLeft: "5px" }} onClick={() => exportar(v.id)}>Exportar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {detalle && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            border: "1px solid #ccc",
            background: "#f7f7f7",
          }}
        >
          <h3>Detalle de versión</h3>
          <pre>{JSON.stringify(detalle, null, 2)}</pre>
          <button onClick={() => setDetalle(null)}>Cerrar</button>
        </div>
      )}
    </div>
  );
}
