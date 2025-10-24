import { useState, useEffect } from 'react';
import { Badge, IconButton, Popover } from '@mui/material';
import { Notifications as NotificationsIcon } from '@mui/icons-material';
import useNotificationStore from '../../stores/notificationStore';
import NotificationDropdown from './NotificationDropdown';

export default function NotificationBell() {
  const [anchorEl, setAnchorEl] = useState(null);
  const { unreadCount, fetchUnreadCount } = useNotificationStore();
  
  // Poll for unread count every 30 seconds
  useEffect(() => {
    fetchUnreadCount();
    const interval = setInterval(() => {
      fetchUnreadCount();
    }, 30000); // 30 seconds
    
    return () => clearInterval(interval);
  }, [fetchUnreadCount]);
  
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleClose = () => {
    setAnchorEl(null);
  };
  
  const open = Boolean(anchorEl);
  
  return (
    <>
      <IconButton
        color="inherit"
        onClick={handleClick}
        aria-label="notifications"
        aria-describedby="notification-popover"
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>
      
      <Popover
        id="notification-popover"
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        PaperProps={{
          sx: {
            width: 400,
            maxHeight: 600,
            mt: 1,
          },
        }}
      >
        <NotificationDropdown onClose={handleClose} />
      </Popover>
    </>
  );
}

