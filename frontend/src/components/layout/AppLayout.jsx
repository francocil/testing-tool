// ============================================================
//  APP LAYOUT - ESTRUCTURA INSTITUCIONAL PRINCIPAL
// ============================================================
//
// Este layout define la estructura visual de TODAS las páginas
// protegidas del sistema.
//
// Comportamiento institucional:
//
// ✔ Sidebar superpuesto (overlay) para reforzar glassmorphism
// ✔ Al hacer clic fuera del sidebar → se cierra automáticamente
// ✔ Header fijo
// ✔ Contenido con margen fijo (sidebar cerrado)
// ✔ Responsive completo
//
// ============================================================

import { Box } from "@mui/material";
import { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function AppLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleSidebar = () => setSidebarOpen((prev) => !prev);

  const closeSidebar = () => setSidebarOpen(false);

  return (
    <Box sx={{ display: "flex", position: "relative" }}>

      {/* HEADER FIJO */}
      <Header onToggleSidebar={toggleSidebar} sidebarOpen={sidebarOpen} />

      {/* SIDEBAR SUPERPUESTO */}
      <Sidebar open={sidebarOpen} />

      {/* OVERLAY PARA CERRAR SIDEBAR */}
      {sidebarOpen && (
        <Box
          onClick={closeSidebar}
          sx={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            zIndex: 998, // ⭐ AHORA SIEMPRE POR ENCIMA DEL CONTENIDO
            backgroundColor: "rgba(0,0,0,0.0)",
          }}
        />
      )}

      {/* CONTENIDO PRINCIPAL */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          mt: 8, // espacio para header fijo

          // Margen fijo del sidebar colapsado
          ml: "70px",

          transition: "margin-left 0.3s ease",

          position: "relative",
          zIndex: 10, // contenido por debajo del overlay

          p: 2,

          // RESPONSIVE
          "@media (max-width: 900px)": {
            ml: "60px",
          },

          "@media (max-width: 600px)": {
            ml: "0px", // en móviles sidebar siempre superpuesto
          },
        }}
      >
        {children}
      </Box>
    </Box>
  );
}
