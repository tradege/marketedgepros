import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import NotificationBell from '../notifications/NotificationBell';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import {
  Menu as MenuIcon,
  Dashboard,
  Person,
  EmojiEvents,
  Description,
  Settings,
  Logout,
  Home,
} from '@mui/icons-material';
import useAuthStore from '../../store/authStore';
import Layout from '../layout/Layout';

const drawerWidth = 260;

const menuItems = [
  { text: 'Dashboard', icon: Dashboard, path: '/dashboard', color: '#667eea' },
  { text: 'Profile', icon: Person, path: '/profile', color: '#f093fb' },
  { text: 'Challenges', icon: EmojiEvents, path: '/challenges', color: '#4facfe' },
  { text: 'Documents', icon: Description, path: '/documents', color: '#43e97b' },
  { text: 'Settings', icon: Settings, path: '/settings', color: '#fa709a' },
];

export default function UserLayout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, isAuthenticated } = useAuthStore();

  // Public pages that should always show Navbar (not sidebar)
  const publicPages = ['/programs', '/program', '/how-it-works', '/about', '/faq', '/contact', '/terms', '/privacy'];
  const isPublicPage = publicPages.some(page => location.pathname.startsWith(page));

  // If user is not authenticated OR on a public page, use public Layout instead
  if (!isAuthenticated || isPublicPage) {
    return <Layout>{children}</Layout>;
  }

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getBreadcrumbs = () => {
    const path = location.pathname;
    const parts = path.split('/').filter(Boolean);
    return parts.map((part, index) => ({
      label: part.charAt(0).toUpperCase() + part.slice(1),
      path: '/' + parts.slice(0, index + 1).join('/'),
    }));
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', bgcolor: '#1a1f2e' }}>
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Avatar
          sx={{
            width: 64,
            height: 64,
            margin: '0 auto',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            fontSize: '2rem',
            fontWeight: 700,
          }}
        >
          {user?.name?.charAt(0) || 'U'}
        </Avatar>
        <Typography variant="h6" sx={{ mt: 2, color: 'white', fontWeight: 600 }}>
          {user?.name || 'User'}
        </Typography>
        <Chip
          label={user?.role || 'Trader'}
          size="small"
          sx={{
            mt: 1,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            fontWeight: 600,
          }}
        />
      </Box>

      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />

      <List sx={{ flex: 1, px: 2, py: 2 }}>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItem key={item.text} disablePadding sx={{ mb: 1 }}>
              <ListItemButton
                onClick={() => navigate(item.path)}
                sx={{
                  borderRadius: 2,
                  bgcolor: isActive ? 'rgba(102, 126, 234, 0.15)' : 'transparent',
                  color: isActive ? item.color : 'rgba(255,255,255,0.7)',
                  '&:hover': {
                    bgcolor: 'rgba(102, 126, 234, 0.1)',
                    color: item.color,
                  },
                  transition: 'all 0.3s',
                }}
              >
                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                  <item.icon />
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  primaryTypographyProps={{
                    fontWeight: isActive ? 600 : 400,
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />

      <Box sx={{ p: 2 }}>
        <ListItemButton
          onClick={handleLogout}
          sx={{
            borderRadius: 2,
            color: 'rgba(255,255,255,0.7)',
            '&:hover': {
              bgcolor: 'rgba(239, 68, 68, 0.1)',
              color: '#ef4444',
            },
          }}
        >
          <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
            <Logout />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItemButton>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#0f1419' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: '#1a1f2e',
          boxShadow: 'none',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Breadcrumbs sx={{ color: 'rgba(255,255,255,0.7)' }}>
            <Link
              underline="hover"
              sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer', color: 'inherit' }}
              onClick={() => navigate('/')}
            >
              <Home sx={{ mr: 0.5, fontSize: 20 }} />
              Home
            </Link>
            {getBreadcrumbs().map((crumb, index) => (
              <Typography key={index} sx={{ color: 'white' }}>
                {crumb.label}
              </Typography>
            ))}
          </Breadcrumbs>
          
          {/* Notifications */}
          <Box sx={{ ml: 'auto' }}>
            <NotificationBell />
          </Box>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
        }}
      >
        {children}
      </Box>
    </Box>
  );
}

