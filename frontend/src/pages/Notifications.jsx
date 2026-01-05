import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, CheckCircle, Settings, Loader } from 'lucide-react';
import useNotificationStore from '../stores/notificationStore';
import { formatDistanceToNow } from '../utils/dateUtils';
import UserLayout from '../components/layout/UserLayout';

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
    low: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
    normal: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    high: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    urgent: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  };
  return colors[priority] || colors.normal;
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
  
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };
  
  const handlePageChange = (page) => {
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
    
    if (notification.type === 'withdrawal') {
      navigate('/trader/withdrawals');
    } else if (notification.type === 'commission') {
      navigate('/affiliate/commissions');
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
  
  const tabs = [
    { label: 'All', value: 'all' },
    { label: 'Unread', value: 'unread' },
    { label: 'Withdrawals', value: 'withdrawal' },
    { label: 'Commissions', value: 'commission' },
    { label: 'KYC', value: 'kyc' },
    { label: 'Payments', value: 'payment' },
    { label: 'Challenges', value: 'challenge' },
    { label: 'System', value: 'system' },
  ];
  
  return (
    <UserLayout>
      <div className="max-w-6xl mx-auto p-6">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">Notifications</h1>
          <div className="flex gap-3">
            <button
              onClick={handleMarkAllAsRead}
              disabled={notifications.length === 0}
              className="flex items-center gap-2 px-4 py-2 border border-white/20 text-white rounded-lg hover:bg-white/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <CheckCircle className="w-4 h-4" />
              Mark All Read
            </button>
            <button
              onClick={() => navigate('/settings/notifications')}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg hover:from-purple-700 hover:to-purple-900 transition-colors"
            >
              <Settings className="w-4 h-4" />
              Settings
            </button>
          </div>
        </div>
        
        <div className="mb-6 bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg p-1">
          <div className="flex gap-1 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.value}
                onClick={() => handleTabChange(tab.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.value
                    ? 'bg-gradient-to-r from-purple-600 to-purple-800 text-white'
                    : 'text-gray-300 hover:text-white hover:bg-white/5'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
        
        <div className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-lg">
          {loading ? (
            <div className="flex justify-center p-12">
              <Loader className="w-8 h-8 text-purple-500 animate-spin" />
            </div>
          ) : notifications.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-400">No notifications found</p>
            </div>
          ) : (
            <>
              <div className="divide-y divide-white/5">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    onClick={() => handleNotificationClick(notification)}
                    className={`flex items-start gap-4 p-4 cursor-pointer transition-colors ${
                      notification.is_read 
                        ? 'hover:bg-white/5' 
                        : 'bg-white/10 hover:bg-white/15'
                    }`}
                  >
                    <div className="text-3xl flex-shrink-0 mt-1">
                      {getNotificationIcon(notification.type)}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className={`text-base ${notification.is_read ? 'text-gray-300' : 'text-white font-semibold'}`}>
                          {notification.title}
                        </h3>
                        <span className={`px-2 py-0.5 text-xs font-medium rounded ${getPriorityColor(notification.priority)}`}>
                          {notification.priority}
                        </span>
                        {!notification.is_read && (
                          <div className="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
                        )}
                      </div>
                      <p className="text-sm text-gray-400 mb-1">
                        {notification.message}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatDistanceToNow(new Date(notification.created_at), { addSuffix: true })}
                      </p>
                    </div>
                    
                    <button
                      onClick={(e) => handleDelete(e, notification.id)}
                      className="flex-shrink-0 p-2 text-gray-400 hover:text-red-400 transition-colors"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                ))}
              </div>
              
              {totalPages > 1 && (
                <div className="flex justify-center gap-2 p-4 border-t border-white/10">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-white/20 text-white rounded-lg hover:bg-white/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  <div className="flex items-center gap-2">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                        className={`w-10 h-10 rounded-lg transition-colors ${
                          currentPage === page
                            ? 'bg-gradient-to-r from-purple-600 to-purple-800 text-white'
                            : 'border border-white/20 text-gray-300 hover:bg-white/10'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 border border-white/20 text-white rounded-lg hover:bg-white/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </UserLayout>
  );
}