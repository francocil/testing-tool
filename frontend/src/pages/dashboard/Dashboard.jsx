// ============================================================
//  DASHBOARD.JSX - PANEL INSTITUCIONAL DEL GOBIERNO DE TUCUMÁN
// ============================================================
//
// Este componente representa el panel principal del sistema.
// Incluye:
//
// - KPI Cards institucionales
// - Status Cards (OK / FAIL / WARNING / Pendientes)
// - Quick Action Cards (Crear Proyecto, Ejecución, Ir a Proyectos)
// - Gráficos institucionales (Pie + Bar)
// - Últimas ejecuciones (NUEVO diseño institucional)
//
// ============================================================

import { useEffect, useState } from "react";
import {
  Typography,
  CircularProgress,
  Box,
  Grid,
  useTheme,
} from "@mui/material";

import {
  fetchProyectos,
  fetchEjecuciones,
} from "../../api/dashboard";

import useAuth from "/src/hooks/useAuth.js";

// ============================================================
//  COMPONENTES INSTITUCIONALES
// ============================================================
import KpiCard from "../../components/dashboard/KpiCard";
import StatusCard from "../../components/dashboard/StatusCard";
import QuickActionCard from "../../components/dashboard/QuickActionCard";
import LastExecutionCard from "../../components/dashboard/LastExecutionCard";
import ResultsPieChart from "../../components/dashboard/ResultsPieChart";
import ResultsBarChart from "../../components/dashboard/ResultsBarChart";

// Íconos MUI
import FolderIcon from "@mui/icons-material/Folder";
import PlayCircleIcon from "@mui/icons-material/PlayCircle";
import BarChartIcon from "@mui/icons-material/BarChart";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import WarningIcon from "@mui/icons-material/Warning";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";

import AddCircleIcon from "@mui/icons-material/AddCircle";
import VisibilityIcon from "@mui/icons-material/Visibility";

export default function Dashboard() {
  const { user, role } = useAuth();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const [loading, setLoading] = useState(true);
  const [proyectos, setProyectos] = useState([]);
  const [ejecuciones, setEjecuciones] = useState([]);
  const [error, setError] = useState(null);

  // ============================================================
  //  CARGA DE DATOS DEL BACKEND
  // ============================================================
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);

        const [proy, ejec] = await Promise.all([
          fetchProyectos(),
          fetchEjecuciones(),
        ]);

        setProyectos(proy);
        setEjecuciones(ejec);
      } catch (err) {
        setError("Error al cargar datos del dashboard");
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // ============================================================
  //  MÉTRICAS PRINCIPALES
  // ============================================================
  const totalProyectos = proyectos.length;
  const totalEjecuciones = ejecuciones.length;

  const ejecucionesOK = ejecuciones.filter((e) => e.resultado_global === "OK").length;
  const ejecucionesFAIL = ejecuciones.filter((e) => e.resultado_global === "FAIL").length;
  const ejecucionesWARNING = ejecuciones.filter((e) => e.resultado_global === "WARNING").length;
  const ejecucionesPEND = ejecuciones.filter((e) => !e.resultado_global).length;

  const porcentajeAceptacionReal =
    totalEjecuciones > 0
      ? ((ejecucionesOK / totalEjecuciones) * 100).toFixed(2)
      : 0;

  // ============================================================
  //  DATOS PARA GRÁFICOS
  // ============================================================
  const pieData = [
    { name: "OK", value: ejecucionesOK },
    { name: "FAIL", value: ejecucionesFAIL },
    { name: "WARNING", value: ejecucionesWARNING },
  ];

  const barData = [
    { name: "OK", cantidad: ejecucionesOK },
    { name: "FAIL", cantidad: ejecucionesFAIL },
    { name: "WARNING", cantidad: ejecucionesWARNING },
  ];
  // ============================================================
  //  RENDER PRINCIPAL
  // ============================================================
  return (
    <Box sx={{ width: "100%" }}>
      
      {/* TÍTULO PRINCIPAL */}
      <Typography
        variant="h4"
        sx={{
          mb: 3,
          fontWeight: 700,
          color: isDark ? "#005CA2" : "#84CFED",
        }}
      >
        Panel de Control
      </Typography>

      {/* BIENVENIDA */}
      <Box sx={{ mb: 3 }}>
        <Typography
          variant="h5"
          sx={{
            fontWeight: 600,
            color: isDark ? "#84CFED" : "#005CA2",
          }}
        >
          Bienvenido, {user?.nombre}
        </Typography>

        <Typography
          variant="subtitle1"
          sx={{
            opacity: 0.9,
            fontWeight: 500,
            color: isDark ? "rgb(132, 207, 237)" : "#005CA2",
          }}
        >
          Rol: {role}
        </Typography>
      </Box>

      {/* LOADING / ERROR */}
      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <>
          {/* ============================================================ */}
          {/*  KPI CARDS */}
          {/* ============================================================ */}
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 4 }}>
              <KpiCard title="Proyectos" value={totalProyectos} icon={<FolderIcon />} />
            </Grid>

            <Grid size={{ xs: 12, md: 4 }}>
              <KpiCard title="Ejecuciones" value={totalEjecuciones} icon={<PlayCircleIcon />} />
            </Grid>

            <Grid size={{ xs: 12, md: 4 }}>
              <KpiCard
                title="Aceptación Global"
                value={`${porcentajeAceptacionReal}%`}
                icon={<BarChartIcon />}
              />
            </Grid>
          </Grid>

          {/* ============================================================ */}
          {/*  STATUS CARDS */}
          {/* ============================================================ */}
          <Typography
            variant="h5"
            sx={{
              mt: 5,
              mb: 2,
              fontWeight: 600,
              color: isDark ? "#84CFED" : "#005CA2",
            }}
          >
            Estado de Ejecuciones
          </Typography>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 3 }}>
              <StatusCard
                title="OK"
                value={ejecucionesOK}
                icon={<CheckCircleIcon />}
                color="#2ecc71"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <StatusCard
                title="FAIL"
                value={ejecucionesFAIL}
                icon={<ErrorIcon />}
                color="#e74c3c"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <StatusCard
                title="WARNING"
                value={ejecucionesWARNING}
                icon={<WarningIcon />}
                color="#f1c40f"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <StatusCard
                title="Pendientes"
                value={ejecucionesPEND}
                icon={<HourglassEmptyIcon />}
                color="#3498db"
              />
            </Grid>
          </Grid>

          {/* ============================================================ */}
          {/*  ACCIONES RÁPIDAS */}
          {/* ============================================================ */}
          <Typography
            variant="h5"
            sx={{
              mt: 5,
              mb: 2,
              fontWeight: 600,
              color: isDark ? "#84CFED" : "#005CA2",
            }}
          >
            Acciones Rápidas
          </Typography>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 3 }}>
              <QuickActionCard
                title="Crear Proyecto"
                icon={<AddCircleIcon />}
                to="/proyectos/crear"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <QuickActionCard
                title="Ir a Proyectos"
                icon={<VisibilityIcon />}
                to="/proyectos"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <QuickActionCard
                title="Crear Ejecución"
                icon={<AddCircleIcon />}
                to="/ejecuciones/crear"
              />
            </Grid>

            <Grid size={{ xs: 12, md: 3 }}>
              <QuickActionCard
                title="Ver Ejecuciones"
                icon={<VisibilityIcon />}
                to="/ejecuciones"
              />
            </Grid>
          </Grid>

          {/* ============================================================ */}
          {/*  GRÁFICOS */}
          {/* ============================================================ */}
          <Grid container spacing={3} sx={{ mt: 4 }}>
            <Grid size={{ xs: 12, md: 6 }}>
              <ResultsPieChart data={pieData} />
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <ResultsBarChart data={barData} />
            </Grid>
          </Grid>

          {/* ============================================================ */}
          {/*  ÚLTIMAS EJECUCIONES */}
          {/* ============================================================ */}
          <Box sx={{ mt: 4 }}>
            <Typography
              variant="h5"
              sx={{
                mb: 2,
                fontWeight: 600,
                color: isDark ? "#84CFED" : "#005CA2",
              }}
            >
              Últimas Ejecuciones
            </Typography>

            <Grid container spacing={2}>
              {ejecuciones.length === 0 ? (
                <Grid size={12}>
                  <Box
                    sx={{
                      p: 4,
                      borderRadius: 3,
                      textAlign: "center",
                      background: isDark
                        ? "rgba(42, 49, 57, 0.35)"
                        : "rgba(255, 255, 255, 0.55)",
                      backdropFilter: "blur(10px)",
                      WebkitBackdropFilter: "blur(10px)",
                      border: isDark ? "1px solid rgba(255,255,255,0.12)" : "none",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 600,
                        color: isDark ? "#84CFED" : "#005CA2",
                      }}
                    >
                      No hay ejecuciones registradas
                    </Typography>

                    <Typography
                      variant="body2"
                      sx={{
                        mt: 1,
                        opacity: 0.8,
                        color: isDark ? "#84CFED" : "#003B70",
                      }}
                    >
                      Cuando se registren ejecuciones, aparecerán aquí.
                    </Typography>

                    <Box sx={{ mt: 3 }}>
                      <QuickActionCard
                        title="Crear Ejecución"
                        icon={<AddCircleIcon />}
                        to="/ejecuciones/crear"
                      />
                    </Box>
                  </Box>
                </Grid>
              ) : (
                ejecuciones.slice(0, 5).map((e) => (
                  <Grid size={{ xs: 12, md: 6 }} key={e.id}>
                    <LastExecutionCard
                      casoId={e.caso_id}
                      resultado={e.resultado_global}
                      fecha={e.fecha}
                    />
                  </Grid>
                ))
              )}
            </Grid>
          </Box>
        </>
      )}
    </Box>
  );
}
