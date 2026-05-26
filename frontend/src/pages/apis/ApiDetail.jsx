import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "../../api/axiosClient";

// 🔥 Import panel de versiones
import ApiVersionList from "./components/ApiVersionList";

// 🔥 Import panel de comparación
import ApiVersionDiff from "./components/ApiVersionDiff";

export default function ApiDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [api, setApi] = useState(null);
  const [parametros, setParametros] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  // TAB actual (0 = info, 1 = parámetros, 2 = versiones, 3 = diff)
  const [tab, setTab] = useState(0);

  // -----------------------------
  // Cargar API + parámetros
  // -----------------------------
  useEffect(() => {
    const loadData = async () => {
      try {
        const resApi = await axios.get(`/apis/${id}`);
        setApi(resApi.data);

        const resParams = await axios.get(`/apis/${id}/parametros`);
        setParametros(resParams.data);
      } catch (err) {
        setErrorMsg("Error cargando API");
      }
      setLoading(false);
    };

    loadData();
  }, [id]);

  if (loading) return <p>Cargando API...</p>;
  if (errorMsg) return <p style={{ color: "red" }}>{errorMsg}</p>;
  if (!api) return <p>No se encontró la API</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Detalle de API</h1>

      <button onClick={() => navigate("/apis")}>Volver</button>
      <button onClick={() => navigate(`/apis/${id}/editar`)}>Editar</button>
      <button onClick={() => navigate(`/apis/tester?api=${id}`)}>
        Probar API
      </button>

      <hr />

      {/* ----------------------------- */}
      {/* TABS */}
      {/* ----------------------------- */}
      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={() => setTab(0)}
          style={{
            marginRight: "10px",
            fontWeight: tab === 0 ? "bold" : "normal",
          }}
        >
          Información
        </button>

        <button
          onClick={() => setTab(1)}
          style={{
            marginRight: "10px",
            fontWeight: tab === 1 ? "bold" : "normal",
          }}
        >
          Parámetros
        </button>

        <button
          onClick={() => setTab(2)}
          style={{
            marginRight: "10px",
            fontWeight: tab === 2 ? "bold" : "normal",
          }}
        >
          Versiones
        </button>

        <button
          onClick={() => setTab(3)}
          style={{
            fontWeight: tab === 3 ? "bold" : "normal",
          }}
        >
          Comparar versiones
        </button>
      </div>

      {/* ----------------------------- */}
      {/* PANEL 0: Información */}
      {/* ----------------------------- */}
      {tab === 0 && (
        <>
          <h2>{api.nombre}</h2>
          <p><strong>Descripción:</strong> {api.descripcion || "—"}</p>

          <p><strong>Método:</strong> {api.metodo}</p>
          <p><strong>Base URL:</strong> {api.base_url || "—"}</p>
          <p><strong>Endpoint:</strong> {api.endpoint}</p>

          <p><strong>Versión:</strong> {api.version}</p>
          <p><strong>Timeout:</strong> {api.timeout_segundos} segundos</p>
          <p><strong>Retries:</strong> {api.retries}</p>
          <p><strong>Activo:</strong> {api.activo ? "Sí" : "No"}</p>

          <hr />

          <h3>Autenticación</h3>
          <p><strong>Tipo:</strong> {api.auth_tipo}</p>
          <pre>{JSON.stringify(api.auth_config, null, 2)}</pre>

          <h3>Headers por defecto</h3>
          <pre>{JSON.stringify(api.headers_por_defecto, null, 2)}</pre>

          <h3>Body ejemplo</h3>
          <pre>{JSON.stringify(api.body_ejemplo, null, 2)}</pre>
        </>
      )}

      {/* ----------------------------- */}
      {/* PANEL 1: Parámetros */}
      {/* ----------------------------- */}
      {tab === 1 && (
        <>
          <h2>Parámetros asociados</h2>

          {parametros.length === 0 ? (
            <p>No hay parámetros asociados.</p>
          ) : (
            <table border="1" cellPadding="8" style={{ width: "100%" }}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Tipo</th>
                  <th>Obligatorio</th>
                  <th>Valor por defecto</th>
                </tr>
              </thead>

              <tbody>
                {parametros.map((p) => (
                  <tr key={p.id}>
                    <td>{p.id}</td>
                    <td>{p.nombre}</td>
                    <td>{p.tipo}</td>
                    <td>{p.obligatorio ? "Sí" : "No"}</td>
                    <td>{p.valor_por_defecto || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      {/* ----------------------------- */}
      {/* PANEL 2: Versiones */}
      {/* ----------------------------- */}
      {tab === 2 && (
        <div>
          <ApiVersionList apiId={id} />
        </div>
      )}

      {/* ----------------------------- */}
      {/* PANEL 3: Comparar versiones */}
      {/* ----------------------------- */}
      {tab === 3 && (
        <div>
          <ApiVersionDiff apiId={id} />
        </div>
      )}
    </div>
  );
}
