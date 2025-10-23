import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Avatar,
  Menu,
  MenuItem,
  Breadcrumbs,
  Link,
  Chip,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  People,
  Assessment,
  Payment,
  VerifiedUser,
  Settings,
  Logout,
  Home,
  ChevronRight,
  Approval,
} from '@mui/icons-material';
import useAuthStore from '../../store/authStore';
import { ROLES, ROLE_CONFIG, getRoleLabel } from '../../constants/roles';
import { getRoleColor } from '../../constants/roleColors';

const drawerWidth = 280;

const menuItems = [
  { title: 'Dashboard', path: '/admin', icon: Dashboard, color: '#667eea' },
  { title: 'Users', path: '/admin/users', icon: People, color: '#f093fb', adminOnly: true },
  { title: 'Programs', path: '/admin/programs', icon: Assessment, color: '#4facfe' },
  { title: 'Payments', path: '/admin/payments', icon: Payment, color: '#43e97b' },
  { title: 'Payment Approvals', path: '/admin/payment-approvals', icon: Approval, color: '#ff6b6b', superAdminOnly: true },
  { title: 'KYC Approval', path: '/admin/kyc', icon: VerifiedUser, color: '#fa709a' },
  { title: 'Settings', path: '/admin/settings', icon: Settings, color: '#a8edea' },
];

// Role colors and labels are now imported from constants/roles.js

export default function AdminLayout({ children }) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleNavigate = (path) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const getBreadcrumbs = () => {
    const paths = location.pathname.split('/').filter(Boolean);
    return paths.map((path, index) => {
      const to = `/${paths.slice(0, index + 1).join('/')}`;
      const label = path.charAt(0).toUpperCase() + path.slice(1);
      return { label, to };
    });
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo */}
      <Box
        sx={{
          p: 3,
          display: 'flex',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <Avatar
          sx={{
            width: 40,
            height: 40,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            fontWeight: 700,
          }}
        >
          P
        </Avatar>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          MarketEdgePros
        </Typography>
      </Box>

      <Divider />

      {/* Navigation Menu */}
      <List sx={{ flex: 1, px: 2, py: 2 }}>
        {menuItems
          .filter(item => {
            // Hide supermaster-only items from non-supermasters
            if (item.superAdminOnly && ![ROLES.SUPERMASTER, ROLES.SUPER_ADMIN].includes(user?.role)) return false;
            // Hide admin-only items (like Users) from agents and traders
            if (item.adminOnly && ![ROLES.SUPERMASTER, ROLES.SUPER_ADMIN, ROLES.MASTER, ROLES.ADMIN].includes(user?.role)) return false;
            return true;
          })
          .map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItem key={item.path} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => handleNavigate(item.path)}
                sx={{
                  borderRadius: 2,
                  backgroundColor: isActive ? `${item.color}20` : 'transparent',
                  '&:hover': {
                    backgroundColor: `${item.color}30`,
                  },
                  transition: 'all 0.2s',
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 40,
                    color: isActive ? item.color : 'text.secondary',
                  }}
                >
                  <item.icon />
                </ListItemIcon>
                <ListItemText
                  primary={item.title}
                  primaryTypographyProps={{
                    fontWeight: isActive ? 600 : 400,
                    color: isActive ? item.color : 'text.primary',
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      <Divider />

      {/* User Profile */}
      <Box sx={{ p: 2 }}>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            p: 2,
            borderRadius: 2,
            backgroundColor: 'background.paper',
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Avatar
            sx={{
              width: 40,
              height: 40,
              background: `linear-gradient(135deg, ${getRoleColor(user?.role)} 0%, ${getRoleColor(user?.role)}80 100%)`,
            }}
          >
            {user?.email?.[0]?.toUpperCase()}
          </Avatar>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="body2" sx={{ fontWeight: 600 }} noWrap>
              {user?.email}
            </Typography>
            <Chip
              label={getRoleLabel(user?.role)}
              size="small"
              sx={{
                height: 20,
                fontSize: '0.7rem',
                mt: 0.5,
                backgroundColor: `${getRoleColor(user?.role)}20`,
                color: getRoleColor(user?.role),
                fontWeight: 600,
              }}
            />
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
          backgroundColor: 'background.paper',
          backgroundImage: 'none',
          borderBottom: '1px solid',
          borderColor: 'divider',
          boxShadow: 'none',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          {/* Breadcrumbs */}
          <Breadcrumbs
            separator={<ChevronRight fontSize="small" />}
            sx={{ flex: 1 }}
          >
            <Link
              underline="hover"
              color="inherit"
              href="/"
              onClick={(e) => {
                e.preventDefault();
                navigate('/');
              }}
              sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
            >
              <Home fontSize="small" />
            </Link>
            {getBreadcrumbs().map((crumb, index) => (
              <Link
                key={index}
                underline="hover"
                color={index === getBreadcrumbs().length - 1 ? 'text.primary' : 'inherit'}
                href={crumb.to}
                onClick={(e) => {
                  e.preventDefault();
                  navigate(crumb.to);
                }}
                sx={{ fontWeight: index === getBreadcrumbs().length - 1 ? 600 : 400 }}
              >
                {crumb.label}
              </Link>
            ))}
          </Breadcrumbs>

          {/* Profile Menu */}
          <IconButton onClick={handleProfileMenuOpen} sx={{ ml: 2 }}>
            <Avatar
              sx={{
                width: 32,
                height: 32,
                background: `linear-gradient(135deg, ${getRoleColor(user?.role)} 0%, ${getRoleColor(user?.role)}80 100%)`,
              }}
            >
              {user?.email?.[0]?.toUpperCase()}
            </Avatar>
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleProfileMenuClose}
          >
            <MenuItem onClick={() => { handleProfileMenuClose(); navigate('/profile'); }}>
              Profile
            </MenuItem>
            <MenuItem onClick={() => { handleProfileMenuClose(); navigate('/admin/settings'); }}>
              Settings
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <Logout fontSize="small" />
              </ListItemIcon>
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              backgroundColor: 'background.default',
            },
          }}
        >
          {drawer}
        </Drawer>

        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              backgroundColor: 'background.default',
              borderRight: '1px solid',
              borderColor: 'divider',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
          backgroundColor: 'background.default',
          minHeight: '100vh',
        }}
      >
        {children}
      </Box>
    </Box>
  );
}

