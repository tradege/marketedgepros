import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, Trash2, Loader } from 'lucide-react';
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
    low: 'bg-gray-400',
    normal: 'bg-blue-500',
    high: 'bg-yellow-500',
    urgent: 'bg-red-500',
  };
  return colors[priority] || 'bg-blue-500';
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
      navigate('/affiliate/commissions');
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
      <div className="flex justify-center p-8">
        <Loader className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    );
  }
  
  return (
    <div className="flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b border-white/10">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5 text-white" />
          <h3 className="text-lg font-semibold text-white">Notifications</h3>
        </div>
        {notifications.length > 0 && (
          <button
            onClick={handleMarkAllAsRead}
            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
          >
            Mark all read
          </button>
        )}
      </div>
      
      {/* Notification List */}
      {notifications.length === 0 ? (
        <div className="p-8 text-center">
          <p className="text-gray-400">No notifications</p>
        </div>
      ) : (
        <div className="max-h-96 overflow-y-auto">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              onClick={() => handleNotificationClick(notification)}
              className={`flex items-start gap-3 p-4 border-b border-white/5 cursor-pointer transition-colors ${
                notification.is_read 
                  ? 'hover:bg-white/5' 
                  : 'bg-white/10 hover:bg-white/15'
              }`}
            >
              {/* Icon */}
              <div className="text-2xl flex-shrink-0">
                {getNotificationIcon(notification.type)}
              </div>
              
              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <p className={`text-sm ${notification.is_read ? 'text-gray-300' : 'text-white font-semibold'}`}>
                    {notification.title}
                  </p>
                  {!notification.is_read && (
                    <div className={`w-2 h-2 rounded-full ${getPriorityColor(notification.priority)}`} />
                  )}
                </div>
                <p className="text-sm text-gray-400 mb-1 line-clamp-2">
                  {notification.message}
                </p>
                <p className="text-xs text-gray-500">
                  {formatDistanceToNow(new Date(notification.created_at), { addSuffix: true })}
                </p>
              </div>
              
              {/* Delete Button */}
              <button
                onClick={(e) => handleDelete(e, notification.id)}
                className="flex-shrink-0 p-1 text-gray-400 hover:text-red-400 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
      
      {/* Footer */}
      {notifications.length > 0 && (
        <div className="p-2 border-t border-white/10">
          <button
            onClick={handleViewAll}
            className="w-full py-2 text-sm text-blue-400 hover:text-blue-300 hover:bg-white/5 rounded transition-colors"
          >
            View All Notifications
          </button>
        </div>
      )}
    </div>
  );
}

