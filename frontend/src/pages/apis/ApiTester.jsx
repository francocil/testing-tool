import { useState } from "react";
import axios from "../../api/axiosClient";

export default function ApiTester() {
  const [metodo, setMetodo] = useState("GET");
  const [baseUrl, setBaseUrl] = useState("");
  const [endpoint, setEndpoint] = useState("");
  const [headers, setHeaders] = useState("{}");
  const [body, setBody] = useState("{}");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const enviar = async () => {
    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post("/apis/test", {
        metodo,
        base_url: baseUrl,
        endpoint,
        headers: headers ? JSON.parse(headers) : {},
        body: body ? JSON.parse(body) : {},
      });

      setResponse(res.data);
    } catch (err) {
      setResponse({
        ok: false,
        status_code: 0,
        body: err.message,
        headers: {},
        elapsed_ms: 0,
      });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Tester de APIs</h1>

      {/* REQUEST */}
      <div style={{ marginBottom: "20px" }}>
        <div style={{ display: "flex", gap: "10px" }}>
          <select
            value={metodo}
            onChange={(e) => setMetodo(e.target.value)}
            style={{ width: "120px" }}
          >
            <option>GET</option>
            <option>POST</option>
            <option>PUT</option>
            <option>DELETE</option>
          </select>

          <input
            type="text"
            placeholder="Base URL (https://api.com)"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            style={{ flex: 1 }}
          />

          <input
            type="text"
            placeholder="/endpoint"
            value={endpoint}
            onChange={(e) => setEndpoint(e.target.value)}
            style={{ flex: 1 }}
          />

          <button onClick={enviar} disabled={loading}>
            {loading ? "Enviando..." : "Enviar"}
          </button>
        </div>

        <div style={{ marginTop: "20px" }}>
          <h3>Headers (JSON)</h3>
          <textarea
            rows={4}
            value={headers}
            onChange={(e) => setHeaders(e.target.value)}
            style={{ width: "100%" }}
          />

          <h3>Body (JSON)</h3>
          <textarea
            rows={6}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            style={{ width: "100%" }}
          />
        </div>
      </div>

      {/* RESPONSE */}
      {response && (
        <div style={{ marginTop: "30px" }}>
          <h2>Respuesta</h2>

          <p>
            <strong>Status:</strong> {response.status_code}
          </p>
          <p>
            <strong>Tiempo:</strong> {response.elapsed_ms} ms
          </p>

          <h3>Headers</h3>
          <pre>{JSON.stringify(response.headers, null, 2)}</pre>

          <h3>Body</h3>
          <pre>{JSON.stringify(response.body, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
