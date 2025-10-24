import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Button,
  IconButton,
  Chip,
  Pagination,
  CircularProgress,
} from '@mui/material';
import {
  Delete as DeleteIcon,
  CheckCircle as CheckCircleIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import useNotificationStore from '../stores/notificationStore';
import { formatDistanceToNow } from '../utils/dateUtils';

const getNotificationIcon = (type) => {
  const icons = {
    withdrawal: '💰',
    commission: '💵',
    kyc: '🆔',
    system: '📢',
    payment: '💳',
    challenge: '🎯',
  };
  return icons[type] || '📬';
};

const getPriorityColor = (priority) => {
  const colors = {
    low: 'default',
    normal: 'primary',
    high: 'warning',
    urgent: 'error',
  };
  return colors[priority] || 'primary';
};

export default function Notifications() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('all');
  
  const {
    notifications,
    loading,
    currentPage,
    totalPages,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
  } = useNotificationStore();
  
  useEffect(() => {
    const filters = {};
    if (activeTab === 'unread') {
      filters.is_read = 'false';
    } else if (activeTab !== 'all') {
      filters.type = activeTab;
    }
    
    fetchNotifications(1, filters);
  }, [activeTab, fetchNotifications]);
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  const handlePageChange = (event, page) => {
    const filters = {};
    if (activeTab === 'unread') {
      filters.is_read = 'false';
    } else if (activeTab !== 'all') {
      filters.type = activeTab;
    }
    
    fetchNotifications(page, filters);
  };
  
  const handleNotificationClick = async (notification) => {
    if (!notification.is_read) {
      await markAsRead(notification.id);
    }
    
    // Navigate based on notification type
    if (notification.type === 'withdrawal') {
      navigate('/trader/withdrawals');
    } else if (notification.type === 'commission') {
      navigate('/agent/commissions');
    } else if (notification.type === 'kyc') {
      navigate('/kyc');
    }
  };
  
  const handleDelete = async (e, notificationId) => {
    e.stopPropagation();
    await deleteNotification(notificationId);
  };
  
  const handleMarkAllAsRead = async () => {
    await markAllAsRead();
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Notifications
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<CheckCircleIcon />}
            onClick={handleMarkAllAsRead}
            disabled={notifications.length === 0}
          >
            Mark All Read
          </Button>
          <Button
            variant="contained"
            startIcon={<SettingsIcon />}
            onClick={() => navigate('/settings/notifications')}
          >
            Settings
          </Button>
        </Box>
      </Box>
      
      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="All" value="all" />
          <Tab label="Unread" value="unread" />
          <Tab label="Withdrawals" value="withdrawal" />
          <Tab label="Commissions" value="commission" />
          <Tab label="KYC" value="kyc" />
          <Tab label="Payments" value="payment" />
          <Tab label="Challenges" value="challenge" />
          <Tab label="System" value="system" />
        </Tabs>
      </Paper>
      
      {/* Notification List */}
      <Paper>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : notifications.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="body1" color="text.secondary">
              No notifications found
            </Typography>
          </Box>
        ) : (
          <>
            <List>
              {notifications.map((notification, index) => (
                <div key={notification.id}>
                  <ListItem
                    button
                    onClick={() => handleNotificationClick(notification)}
                    sx={{
                      backgroundColor: notification.is_read ? 'transparent' : 'action.hover',
                      '&:hover': {
                        backgroundColor: 'action.selected',
                      },
                    }}
                  >
                    <ListItemIcon sx={{ fontSize: 32, minWidth: 56 }}>
                      {getNotificationIcon(notification.type)}
                    </ListItemIcon>
                    
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                          <Typography
                            variant="body1"
                            sx={{
                              fontWeight: notification.is_read ? 'normal' : 'bold',
                              flex: 1,
                            }}
                          >
                            {notification.title}
                          </Typography>
                          <Chip
                            label={notification.priority}
                            size="small"
                            color={getPriorityColor(notification.priority)}
                          />
                          {!notification.is_read && (
                            <Box
                              sx={{
                                width: 10,
                                height: 10,
                                borderRadius: '50%',
                                backgroundColor: 'primary.main',
                              }}
                            />
                          )}
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                            {notification.message}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {formatDistanceToNow(new Date(notification.created_at), {
                              addSuffix: true,
                            })}
                          </Typography>
                        </Box>
                      }
                    />
                    
                    <IconButton
                      onClick={(e) => handleDelete(e, notification.id)}
                      sx={{ ml: 2 }}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItem>
                  
                  {index < notifications.length - 1 && <Box sx={{ borderBottom: 1, borderColor: 'divider' }} />}
                </div>
              ))}
            </List>
            
            {/* Pagination */}
            {totalPages > 1 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                <Pagination
                  count={totalPages}
                  page={currentPage}
                  onChange={handlePageChange}
                  color="primary"
                />
              </Box>
            )}
          </>
        )}
      </Paper>
    </Container>
  );
}

