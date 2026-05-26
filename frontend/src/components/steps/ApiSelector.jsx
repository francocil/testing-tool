import { useEffect, useState } from "react";
import axios from "../../services/axiosClient";

export default function ApiSelector({ value, onChange }) {
  const [apis, setApis] = useState([]);

  useEffect(() => {
    const loadApis = async () => {
      try {
        const res = await axios.get("/apis");
        setApis(res.data);
      } catch (err) {
        console.error("Error cargando APIs");
      }
    };

    loadApis();
  }, []);

  return (
    <div>
      <label>API asociada</label>
      <select value={value || ""} onChange={(e) => onChange(e.target.value)}>
        <option value="">— Ninguna —</option>

        {apis.map((api) => (
          <option key={api.id} value={api.id}>
            {api.nombre} ({api.metodo} {api.endpoint})
          </option>
        ))}
      </select>
    </div>
  );
}
