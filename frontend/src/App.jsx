// ============================================================
//  APP.JSX - PUNTO DE ENTRADA DEL SISTEMA DE RUTAS
// ============================================================
//
// Este archivo solo monta AppRouter.
// Toda la lógica de rutas, roles, protección y layout
// está centralizada en src/router/AppRouter.jsx.
//
// ============================================================

import AppRouter from "./router/AppRouter";

export default function App() {
  return <AppRouter />;
}
