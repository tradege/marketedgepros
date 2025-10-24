import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Button,
  Divider,
  CircularProgress,
  IconButton,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Delete as DeleteIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import useNotificationStore from '../../stores/notificationStore';
import { formatDistanceToNow } from '../../utils/dateUtils';

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
    low: 'text.secondary',
    normal: 'primary.main',
    high: 'warning.main',
    urgent: 'error.main',
  };
  return colors[priority] || 'primary.main';
};

export default function NotificationDropdown({ onClose }) {
  const navigate = useNavigate();
  const {
    notifications,
    loading,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
  } = useNotificationStore();
  
  useEffect(() => {
    fetchNotifications(1, { per_page: 10 });
  }, [fetchNotifications]);
  
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
    
    onClose();
  };
  
  const handleMarkAllAsRead = async () => {
    await markAllAsRead();
  };
  
  const handleDelete = async (e, notificationId) => {
    e.stopPropagation();
    await deleteNotification(notificationId);
  };
  
  const handleViewAll = () => {
    navigate('/notifications');
    onClose();
  };
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <NotificationsIcon /> Notifications
        </Typography>
        {notifications.length > 0 && (
          <Button size="small" onClick={handleMarkAllAsRead}>
            Mark all read
          </Button>
        )}
      </Box>
      
      <Divider />
      
      {/* Notification List */}
      {notifications.length === 0 ? (
        <Box sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            No notifications
          </Typography>
        </Box>
      ) : (
        <List sx={{ p: 0, maxHeight: 400, overflow: 'auto' }}>
          {notifications.map((notification) => (
            <ListItem
              key={notification.id}
              button
              onClick={() => handleNotificationClick(notification)}
              sx={{
                backgroundColor: notification.is_read ? 'transparent' : 'action.hover',
                '&:hover': {
                  backgroundColor: 'action.selected',
                },
              }}
            >
              <ListItemIcon sx={{ fontSize: 24 }}>
                {getNotificationIcon(notification.type)}
              </ListItemIcon>
              
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography
                      variant="body2"
                      sx={{
                        fontWeight: notification.is_read ? 'normal' : 'bold',
                        flex: 1,
                      }}
                    >
                      {notification.title}
                    </Typography>
                    {!notification.is_read && (
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          backgroundColor: getPriorityColor(notification.priority),
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
                      {formatDistanceToNow(new Date(notification.created_at), { addSuffix: true })}
                    </Typography>
                  </Box>
                }
              />
              
              <IconButton
                size="small"
                onClick={(e) => handleDelete(e, notification.id)}
                sx={{ ml: 1 }}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </ListItem>
          ))}
        </List>
      )}
      
      {/* Footer */}
      {notifications.length > 0 && (
        <>
          <Divider />
          <Box sx={{ p: 1, textAlign: 'center' }}>
            <Button fullWidth onClick={handleViewAll}>
              View All Notifications
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
}

