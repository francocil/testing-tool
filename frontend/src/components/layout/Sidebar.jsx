// ============================================================
//  SIDEBAR INSTITUCIONAL - PERMISOS EFECTIVOS
// ============================================================
//
// Usa PermissionContext:
//   const { can, hasRole } = usePermission();
//
// Cada item puede definir:
//   - permiso: "ver_proyectos"
//   - permisos: ["ver_proyectos", "ver_modulos"]
//   - roles: ["Administrador"]  <-- nombre REAL del backend
//
// ============================================================

import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
  useTheme,
  Tooltip,
  ListSubheader,
  Divider,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import AssignmentIcon from "@mui/icons-material/Assignment";
import DashboardCustomizeIcon from "@mui/icons-material/DashboardCustomize";
import PeopleIcon from "@mui/icons-material/People";
import SettingsIcon from "@mui/icons-material/Settings";

import { useNavigate, useLocation } from "react-router-dom";
import { usePermission } from "../../context/PermissionContext";

const drawerWidth = 240;
const collapsedWidth = 70;

export default function Sidebar({ open }) {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const { can, hasRole } = usePermission();

  const glassBackground =
    theme.palette.mode === "light"
      ? "rgba(255, 255, 255, 0.55)"
      : "rgba(0, 0, 0, 0.35)";

  // ============================================================
  // SECCIONES DEL SIDEBAR BASADAS EN PERMISOS
  // ============================================================
  const sections = [
  {
    title: "General",
    items: [
      {
        label: "Dashboard",
        icon: <DashboardIcon />,
        path: "/",
        permiso: "auditoria_ver",   // ← PERMISO REAL
      },
    ],
  },

  {
    title: "Gestión",
    items: [
      {
        label: "Proyectos",
        icon: <AssignmentIcon />,
        path: "/proyectos",
        permiso: "proyecto_ver_todos",   // ← PERMISO REAL
      },
    ],
  },

  {
    title: "Administración",
    items: [
      {
        label: "Dash. Administración",
        icon: <DashboardCustomizeIcon />,
        path: "/admin",
        permiso: "seguridad_permiso_ver",   // ← PERMISO REAL
      },
      {
        label: "Agentes",
        icon: <PeopleIcon />,
        path: "/administracion/agentes",
        permiso: "seguridad_usuario_ver",   // ← PERMISO REAL
      },
      {
        label: "Parámetros",
        icon: <SettingsIcon />,
        path: "/administracion/parametros",
        permiso: "seguridad_permiso_ver",   // ← PERMISO REAL
      },
    ],
  },
];

  // ============================================================
  // FILTRADO INSTITUCIONAL
  // ============================================================
  const isVisible = (item) => {
    if (item.permiso && !can(item.permiso)) return false;

    if (item.permisos) {
      const ok = item.permisos.some((p) => can(p));
      if (!ok) return false;
    }

    // 🔥 CORREGIDO: roles seguro + nombres reales
    if (item.roles?.length) {
      const ok = item.roles.some((r) => hasRole(r));
      if (!ok) return false;
    }

    return true;
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        position: "fixed",
        height: "100vh",
        width: open ? drawerWidth : collapsedWidth,
        flexShrink: 0,
        whiteSpace: "nowrap",
        transition: "width 0.3s ease",
        zIndex: (theme) => theme.zIndex.appBar - 1,

        "& .MuiDrawer-paper": {
          position: "fixed",
          height: "100vh",
          width: open ? drawerWidth : collapsedWidth,
          transition: "width 0.3s ease",
          overflowX: "hidden",
          boxSizing: "border-box",

          background: glassBackground,
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",

          borderRight: `1px solid ${theme.palette.divider}`,
          zIndex: (theme) => theme.zIndex.appBar - 1,
          display: "flex",
          flexDirection: "column",
        },
      }}
    >
      <Toolbar />

      <Box sx={{ overflow: "auto", flexGrow: 1 }}>
        {sections.map((section) => {
          const visibleItems = section.items.filter(isVisible);

          if (visibleItems.length === 0) return null;

          return (
            <List
              key={section.title}
              subheader={
                open ? (
                  <ListSubheader
                    sx={{
                      bgcolor: "transparent",
                      color: theme.palette.primary.main,
                      fontWeight: 700,
                      fontSize: "0.9rem",
                    }}
                  >
                    {section.title}
                  </ListSubheader>
                ) : null
              }
            >
              {visibleItems.map((item) => {
                // 🔥 CORREGIDO: rutas dinámicas
                const isActive = location.pathname.startsWith(item.path);

                const button = (
                  <ListItemButton
                    key={item.path}
                    onClick={() => navigate(item.path)}
                    selected={isActive}
                    sx={{
                      px: open ? 2 : 1,
                      justifyContent: open ? "flex-start" : "center",
                      position: "relative",
                      transition: "all 0.3s ease",

                      "&.Mui-selected": {
                        backgroundColor: theme.palette.action.selected,
                      },

                      "&.Mui-selected::before": {
                        content: '""',
                        position: "absolute",
                        left: 0,
                        top: 0,
                        bottom: 0,
                        width: "4px",
                        backgroundColor: theme.palette.primary.main,
                        borderRadius: "0 4px 4px 0",
                        transition: "all 0.3s ease",
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        color: theme.palette.primary.main,
                        minWidth: open ? 40 : "auto",
                        justifyContent: "center",
                      }}
                    >
                      {item.icon}
                    </ListItemIcon>

                    {open && <ListItemText primary={item.label} />}
                  </ListItemButton>
                );

                return open ? (
                  button
                ) : (
                  <Tooltip key={item.path} title={item.label} placement="right">
                    {button}
                  </Tooltip>
                );
              })}
            </List>
          );
        })}
      </Box>

      <Divider />

      <Box
        sx={{
          p: 2,
          textAlign: "center",
          opacity: 0.9,
        }}
      >
        <img
          src="/EscudoTucuman.png"
          alt="Escudo Tucumán"
          style={{
            height: open ? "auto" : "30px",
            maxHeight: "30px",
            width: "auto",
            objectFit: "contain",
            transition: "all 0.3s ease",
            display: "block",
            margin: "0 auto",
          }}
        />
      </Box>
    </Drawer>
  );
}
