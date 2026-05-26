// ============================================================
//  HEADER INSTITUCIONAL - GOBIERNO DE TUCUMÁN (BLUR GLASS)
// ============================================================

import { useContext, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Box,
  Tooltip,
  useTheme,
  Divider,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";

import { ThemeModeContext } from "../../main";
import useLogout from "../../hooks/useLogout";
import { useSelector } from "react-redux";

export default function Header({ onToggleSidebar, sidebarOpen }) {
  const theme = useTheme();
  const { mode, toggleMode } = useContext(ThemeModeContext);

  const logout = useLogout();

  const { user, role } = useSelector((state) => state.auth);

  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleMenuOpen = (event) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);

  const glassBackground =
    theme.palette.mode === "light"
      ? "rgba(255, 255, 255, 0.55)"
      : "rgba(0, 0, 0, 0.35)";

  // Iniciales del usuario
  const initials = user
    ? `${user.nombre?.[0] || ""}${user.apellido?.[0] || ""}`.toUpperCase()
    : "";

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 2,
        background: glassBackground,
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        borderBottom: `1px solid ${theme.palette.divider}`,
        color: theme.palette.text.primary,
      }}
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        
        {/* BOTÓN + LOGO + TÍTULO */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <IconButton
            onClick={onToggleSidebar}
            color="inherit"
            sx={{
              transition: "transform 0.3s ease, opacity 0.2s ease",
              transform: sidebarOpen ? "rotate(0deg)" : "rotate(-90deg)",
              "&:hover": {
                opacity: 0.8,
                transform: sidebarOpen
                  ? "scale(1.05)"
                  : "rotate(-90deg) scale(1.05)",
              },
            }}
          >
            <MenuIcon />
          </IconButton>

          <img
            src="/logo-gobierno-azul.png"
            alt="Gobierno de Tucumán"
            draggable="false"
            style={{
              height: 60,
              opacity: 0.9,
              userSelect: "none",
              pointerEvents: "none",
            }}
          />

          <Typography
            variant="h6"
            sx={{
              fontWeight: 800,
              color: "#84CFED",
            }}
          >
            Quality Assurance Tool
          </Typography>
        </Box>

        {/* ACCIONES */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          
          {/* Toggle modo claro/oscuro */}
          <Tooltip title="Cambiar modo">
            <IconButton onClick={toggleMode} color="inherit">
              {mode === "light" ? <DarkModeIcon /> : <LightModeIcon />}
            </IconButton>
          </Tooltip>

          {/* Avatar */}
          <Tooltip title="Cuenta">
            <IconButton onClick={handleMenuOpen} color="inherit">
              <Avatar sx={{ bgcolor: "#005CA2", fontWeight: 700 }}>
                {initials || "?"}
              </Avatar>
            </IconButton>
          </Tooltip>

          {/* Menú */}
          <Menu
            anchorEl={anchorEl}
            open={open}
            onClose={handleMenuClose}
            anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
            transformOrigin={{ vertical: "top", horizontal: "right" }}
            PaperProps={{
              sx: {
                mt: 1,
                borderRadius: 2,
                minWidth: 200,
                p: 1,
              },
            }}
          >
            {/* Datos del usuario */}
            {user && (
              <Box sx={{ px: 2, py: 1 }}>
                <Typography sx={{ fontWeight: 700 }}>
                  {user.nombre} {user.apellido}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.7 }}>
                  {user.email}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.7 }}>
                  Rol: {role}
                </Typography>
              </Box>
            )}

            <Divider sx={{ my: 1 }} />

            <MenuItem
              onClick={() => {
                handleMenuClose();
                logout();
              }}
            >
              Cerrar sesión
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
