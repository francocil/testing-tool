import { useEffect, useState } from "react";
import axios from "../../../api/axiosClient";

export default function ApiVersionDiff({ apiId }) {
  const [versiones, setVersiones] = useState([]);
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [diff, setDiff] = useState(null);

  useEffect(() => {
    const load = async () => {
      const res = await axios.get(`/apis/versiones/by-api/${apiId}`);
      setVersiones(res.data);
    };
    load();
  }, [apiId]);

  const comparar = async () => {
    if (!a || !b) {
      alert("Seleccioná dos versiones");
      return;
    }

    const resA = await axios.get(`/apis/versiones/${a}`);
    const resB = await axios.get(`/apis/versiones/${b}`);

    const objA = resA.data;
    const objB = resB.data;

    const resultado = [];
    const keys = new Set([...Object.keys(objA), ...Object.keys(objB)]);

    keys.forEach((k) => {
      const valA = objA[k];
      const valB = objB[k];

      if (JSON.stringify(valA) !== JSON.stringify(valB)) {
        resultado.push({
          campo: k,
          antes: valA,
          despues: valB,
        });
      }
    });

    setDiff(resultado);
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Comparar versiones</h2>

      <div style={{ display: "flex", gap: "20px", marginBottom: "10px" }}>
        <div>
          <label>Versión A:</label>
          <br />
          <select value={a} onChange={(e) => setA(e.target.value)}>
            <option value="">Seleccionar</option>
            {versiones.map((v) => (
              <option key={v.id} value={v.id}>
                {v.id} - {v.version}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Versión B:</label>
          <br />
          <select value={b} onChange={(e) => setB(e.target.value)}>
            <option value="">Seleccionar</option>
            {versiones.map((v) => (
              <option key={v.id} value={v.id}>
                {v.id} - {v.version}
              </option>
            ))}
          </select>
        </div>

        <button onClick={comparar}>Comparar</button>
      </div>

      {diff && diff.length > 0 && (
        <table border="1" cellPadding="8" style={{ width: "100%", marginTop: "20px" }}>
          <thead>
            <tr>
              <th>Campo</th>
              <th>Antes</th>
              <th>Después</th>
            </tr>
          </thead>

          <tbody>
            {diff.map((d, i) => (
              <tr key={i}>
                <td><strong>{d.campo}</strong></td>
                <td style={{ background: "#ffecec" }}>
                  {JSON.stringify(d.antes, null, 2)}
                </td>
                <td style={{ background: "#e8ffe8" }}>
                  {JSON.stringify(d.despues, null, 2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {diff && diff.length === 0 && (
        <p>No hay diferencias entre las versiones seleccionadas.</p>
      )}
    </div>
  );
}
