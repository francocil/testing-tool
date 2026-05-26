// ============================================================
// LOGIN.JSX - FORMULARIO GLASS INSTITUCIONAL (SIN MUI, SIN THEME)
// ============================================================
//
// - Fondo institucional radial
// - Patrón institucional desde /public/patterns
// - No depende del theme
// - No usa MUI
// - Estilo glass institucional
//
// ============================================================

import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { loginRequest } from "../../api/auth";
import { loginSuccess } from "../../store/authSlice";
import { useNavigate } from "react-router-dom";

// ------------------------------------------------------------
// ESCUDO INSTITUCIONAL (decoración superior)
// ------------------------------------------------------------
const LogoEscudoBlanco = () => (
  <img
    src="/EscudoTucuman-white.png"
    alt="Escudo Tucumán"
    style={{
      width: "120px",
      height: "auto",
      opacity: 0.9,
      filter: "drop-shadow(0 0 6px rgba(0,0,0,0.25))",
      userSelect: "none",
      pointerEvents: "none",
      cursor: "default",
    }}
  />
);

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  // ------------------------------------------------------------
  // FONDO INSTITUCIONAL + PATRÓN HEXAGONAL EN EL <body>
  // ------------------------------------------------------------
  useEffect(() => {
    document.body.style.margin = "0";
    document.body.style.padding = "0";
    document.body.style.height = "100vh";
    document.body.style.width = "100%";

    document.body.style.backgroundImage =
      'radial-gradient(circle at center, #05365c 0%, rgba(32, 79, 129, 0.77) 100%), url("/patterns/pattern-dark.svg")';

    document.body.style.backgroundAttachment = "fixed";
    document.body.style.backgroundSize = "cover, 140px";
    document.body.style.backgroundRepeat = "no-repeat, repeat";
    document.body.style.backgroundColor = "transparent";

    return () => {
      document.body.style.backgroundImage = "";
      document.body.style.backgroundAttachment = "";
      document.body.style.backgroundSize = "";
      document.body.style.backgroundRepeat = "";
      document.body.style.backgroundColor = "";
      document.body.style.height = "";
      document.body.style.width = "";
    };
  }, []);

  // ------------------------------------------------------------
  // ANIMACIÓN DE ENTRADA
  // ------------------------------------------------------------
  useEffect(() => {
    const styles = `
      @keyframes fadeSlide {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
      }
    `;
    const styleTag = document.createElement("style");
    styleTag.innerHTML = styles;
    document.head.appendChild(styleTag);

    return () => {
      document.head.removeChild(styleTag);
    };
  }, []);

  // ------------------------------------------------------------
  // SUBMIT DEL LOGIN
  // ------------------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // 🔥 Evita que axiosClient envíe un token viejo al backend
    localStorage.removeItem("token");

    try {
      const data = await loginRequest(email, password);

      dispatch(
        loginSuccess({
          access_token: data.access_token,
          usuario: data.usuario,
        })
      );

      navigate("/");
    } catch (err) {
      setError("Credenciales incorrectas");
    }
  };
  // ------------------------------------------------------------
  // RENDER
  // ------------------------------------------------------------
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "16px",
        userSelect: "none",
        cursor: "default",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "420px",
          padding: "24px 28px",
          borderRadius: "16px",
          animation: "fadeSlide 0.6s ease-out",
          background: "rgba(255, 255, 255, 0.18)",
          backdropFilter: "blur(18px)",
          WebkitBackdropFilter: "blur(18px)",
          border: "1px solid rgba(255, 255, 255, 0.35)",
          boxShadow: "0 8px 30px rgba(0,0,0,0.25)",
          color: "#FFFFFF",
          userSelect: "none",
          cursor: "default",
          pointerEvents: "auto",
        }}
      >
        {/* ESCUDO */}
        <div style={{ textAlign: "center", marginBottom: "18px" }}>
          <LogoEscudoBlanco />
        </div>

        <h1
          style={{
            margin: "0 0 16px 0",
            textAlign: "center",
            fontSize: "22px",
            fontWeight: 800,
            letterSpacing: "0.5px",
          }}
        >
          Iniciar Sesión
        </h1>

        {error && (
          <div
            style={{
              marginBottom: "12px",
              padding: "8px 10px",
              borderRadius: "8px",
              background: "rgba(255,0,0,0.25)",
              border: "1px solid rgba(255,255,255,0.3)",
              color: "#FFFFFF",
              fontSize: "14px",
            }}
          >
            {error}
          </div>
        )}

        {/* FORMULARIO */}
        <form
          onSubmit={handleSubmit}
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "14px",
            userSelect: "none",
          }}
        >
          {/* EMAIL */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label
              htmlFor="email"
              style={{
                fontSize: "14px",
                color: "rgba(255,255,255,0.85)",
              }}
            >
              Email *
            </label>

            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              style={{
                width: "100%",
                padding: "10px 12px",
                borderRadius: "10px",
                border: "1px solid rgba(255,255,255,0.4)",
                background: "rgba(255,255,255,0.1)",
                color: "#FFFFFF",
                fontSize: "14px",
                outline: "none",
                userSelect: "text",
                cursor: "text",
              }}
            />
          </div>

          {/* PASSWORD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label
              htmlFor="password"
              style={{
                fontSize: "14px",
                color: "rgba(255,255,255,0.85)",
              }}
            >
              Contraseña *
            </label>

            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              style={{
                width: "100%",
                padding: "10px 12px",
                borderRadius: "10px",
                border: "1px solid rgba(255,255,255,0.4)",
                background: "rgba(255,255,255,0.1)",
                color: "#FFFFFF",
                fontSize: "14px",
                outline: "none",
                userSelect: "text",
                cursor: "text",
              }}
            />
          </div>

          {/* BOTÓN */}
          <button
            type="submit"
            style={{
              marginTop: "4px",
              width: "100%",
              padding: "10px 0",
              borderRadius: "10px",
              border: "none",
              backgroundColor: "#0077C8",
              color: "#FFFFFF",
              fontWeight: 700,
              fontSize: "15px",
              cursor: "pointer",
              userSelect: "none",
            }}
          >
            Entrar
          </button>
        </form>

        {/* LINK RECUPERAR */}
        <div
          style={{
            marginTop: "12px",
            textAlign: "center",
            userSelect: "none",
          }}
        >
          <span
            style={{
              fontSize: "13px",
              color: "#84CFED",
              textDecoration: "underline",
              cursor: "pointer",
            }}
            onClick={() => navigate("/recuperar")}
          >
            ¿Olvidaste tu contraseña?
          </span>
        </div>

        {/* LOGOS INSTITUCIONALES */}
        <div
          style={{
            marginTop: "20px",
            textAlign: "center",
            fontSize: "11px",
            opacity: 0.9,
            userSelect: "none",
          }}
        >
          <img
            src="/logo-gobierno.png"
            alt="Gobierno de Tucumán"
            style={{ width: 180, opacity: 0.9, marginBottom: "6px" }}
          />

          <div>Ministerio de Economía y Producción</div>
          <div>Dirección General de Innovación y Desarrollo Digital</div>
        </div>
      </div>
    </div>
  );
}
