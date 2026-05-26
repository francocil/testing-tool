// ============================================================
//  APP ROUTER - SISTEMA DE RUTAS BASADO EN AUTENTICACIÓN Y PERMISOS
// ============================================================

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/dashboard/Dashboard";
import Unauthorized from "../pages/unauthorized/Unauthorized";

import ProtectedRoute from "./ProtectedRoute";
import PermissionGuard from "../guards/PermissionGuard";
import AppLayout from "../components/layout/AppLayout";

// ADMINISTRACIÓN
import AdminDashboard from "../pages/administracion/AdminDashboard";
import Agentes from "../pages/administracion/Agentes";
import Parametros from "../pages/administracion/Parametros";

// PROYECTOS
import ProjectList from "../pages/proyectos/ProjectList";
import ProjectForm from "../pages/proyectos/ProjectForm";
import ProjectDetail from "../pages/proyectos/ProjectDetail";

// MÓDULOS
import ModuleForm from "../pages/modulos/ModuleForm";
import ModuleDetail from "../pages/modulos/ModuleDetail";

// CASOS DE PRUEBA
import CaseList from "../pages/casos/CaseList";
import CaseForm from "../pages/casos/CaseForm";
import CaseDetail from "../pages/casos/CaseDetail";

// PASOS
import StepDetail from "../components/steps/StepDetail";

// EJECUCIÓN
import CaseExecution from "../pages/casos/CaseExecution";

// APIs
import ApiList from "../pages/apis/ApiList";
import ApiForm from "../pages/apis/ApiForm";
import ApiDetail from "../pages/apis/ApiDetail";
import ApiTester from "../pages/apis/ApiTester";

// Versionado de APIs
import ApiVersionList from "../pages/apis/components/ApiVersionList";
import ApiVersionDiff from "../pages/apis/components/ApiVersionDiff";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>

        {/* ===================================================== */}
        {/* RUTAS PÚBLICAS */}
        {/* ===================================================== */}
        <Route path="/login" element={<Login />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* ===================================================== */}
        {/* DASHBOARD */}
        {/* ===================================================== */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="auditoria_ver">
                <AppLayout>
                  <Dashboard />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* ADMINISTRACIÓN */}
        {/* ===================================================== */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="seguridad_permiso_ver">
                <AppLayout>
                  <AdminDashboard />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/administracion/agentes"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="seguridad_usuario_ver">
                <AppLayout>
                  <Agentes />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/administracion/parametros"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="seguridad_permiso_ver">
                <AppLayout>
                  <Parametros />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* PROYECTOS */}
        {/* ===================================================== */}
        <Route
          path="/proyectos"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="proyecto_ver_todos">
                <AppLayout>
                  <ProjectList />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/crear"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="proyecto_crear">
                <AppLayout>
                  <ProjectForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="proyecto_ver_todos">
                <AppLayout>
                  <ProjectDetail />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/editar"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="proyecto_editar">
                <AppLayout>
                  <ProjectForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* MÓDULOS */}
        {/* ===================================================== */}
        <Route
          path="/proyectos/:id/modulos/crear"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="modulo_crear">
                <AppLayout>
                  <ModuleForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/modulos/:moduloId"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="modulo_ver">
                <AppLayout>
                  <ModuleDetail />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/modulos/:moduloId/editar"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="modulo_editar">
                <AppLayout>
                  <ModuleForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* CASOS DE PRUEBA */}
        {/* ===================================================== */}
        <Route
          path="/proyectos/:id/modulos/:moduloId/casos"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="caso_ver_modulo">
                <AppLayout>
                  <CaseList />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/modulos/:moduloId/casos/crear"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="caso_crear">
                <AppLayout>
                  <CaseForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/modulos/:moduloId/casos/:casoId"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="caso_ver_modulo">
                <AppLayout>
                  <CaseDetail />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/proyectos/:id/modulos/:moduloId/casos/:casoId/editar"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="caso_editar">
                <AppLayout>
                  <CaseForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* EJECUCIÓN */}
        {/* ===================================================== */}
        <Route
          path="/proyectos/:id/modulos/:moduloId/casos/:casoId/ejecucion"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="ejecucion_ejecutar">
                <AppLayout>
                  <CaseExecution />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* PASOS */}
        {/* ===================================================== */}
        <Route
          path="/proyectos/:id/modulos/:moduloId/casos/:casoId/pasos/:pasoId"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="paso_ver_caso">
                <AppLayout>
                  <StepDetail />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* EJECUCIONES */}
        {/* ===================================================== */}
        <Route
          path="/ejecuciones"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="ejecucion_ver_todos">
                <AppLayout>
                  <div>Ejecuciones</div>
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/ejecuciones/crear"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="ejecucion_crear">
                <AppLayout>
                  <div>Crear Ejecución (placeholder)</div>
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* APIs */}
        {/* ===================================================== */}
        <Route
          path="/apis"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_ver">
                <AppLayout>
                  <ApiList />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/nueva"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_crear">
                <AppLayout>
                  <ApiForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/:apiId"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_ver">
                <AppLayout>
                  <ApiDetail />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/:apiId/editar"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_editar">
                <AppLayout>
                  <ApiForm />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/tester"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_probar">
                <AppLayout>
                  <ApiTester />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/:apiId/versiones"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_versionar">
                <AppLayout>
                  <ApiVersionList />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        <Route
          path="/apis/versiones/comparar"
          element={
            <ProtectedRoute>
              <PermissionGuard permiso="api_versionar">
                <AppLayout>
                  <ApiVersionDiff />
                </AppLayout>
              </PermissionGuard>
            </ProtectedRoute>
          }
        />

        {/* ===================================================== */}
        {/* 404 */}
        {/* ===================================================== */}
        <Route path="*" element={<Unauthorized />} />

      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
