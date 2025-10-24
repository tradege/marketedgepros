import { create } from 'zustand';
import api from '../services/api';

const useNotificationStore = create((set, get) => ({
  // State
  notifications: [],
  unreadCount: 0,
  preferences: null,
  loading: false,
  error: null,
  
  // Pagination
  currentPage: 1,
  totalPages: 1,
  perPage: 50,
  
  // Filters
  filters: {
    type: null,
    is_read: null,
    priority: null,
  },
  
  // Actions
  fetchNotifications: async (page = 1, filters = {}) => {
    set({ loading: true, error: null });
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: get().perPage.toString(),
        ...filters,
      });
      
      const response = await api.get(`/notifications?${params}`);
      
      set({
        notifications: response.data.notifications,
        currentPage: response.data.page,
        totalPages: response.data.pages,
        filters,
        loading: false,
      });
    } catch (error) {
      set({ error: error.message, loading: false });
      console.error('Failed to fetch notifications:', error);
    }
  },
  
  fetchUnreadCount: async () => {
    try {
      const response = await api.get('/notifications/unread-count');
      set({ unreadCount: response.data.count });
    } catch (error) {
      console.error('Failed to fetch unread count:', error);
    }
  },
  
  markAsRead: async (notificationId) => {
    try {
      await api.post(`/notifications/${notificationId}/read`);
      
      // Update local state
      set((state) => ({
        notifications: state.notifications.map((n) =>
          n.id === notificationId ? { ...n, is_read: true } : n
        ),
        unreadCount: Math.max(0, state.unreadCount - 1),
      }));
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  },
  
  markAllAsRead: async () => {
    try {
      await api.post('/notifications/read-all');
      
      // Update local state
      set((state) => ({
        notifications: state.notifications.map((n) => ({ ...n, is_read: true })),
        unreadCount: 0,
      }));
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error);
    }
  },
  
  deleteNotification: async (notificationId) => {
    try {
      await api.delete(`/notifications/${notificationId}`);
      
      // Update local state
      set((state) => ({
        notifications: state.notifications.filter((n) => n.id !== notificationId),
      }));
    } catch (error) {
      console.error('Failed to delete notification:', error);
    }
  },
  
  fetchPreferences: async () => {
    try {
      const response = await api.get('/notifications/preferences');
      set({ preferences: response.data });
    } catch (error) {
      console.error('Failed to fetch preferences:', error);
    }
  },
  
  updatePreferences: async (preferences) => {
    try {
      const response = await api.put('/notifications/preferences', preferences);
      set({ preferences: response.data.preferences });
      return true;
    } catch (error) {
      console.error('Failed to update preferences:', error);
      return false;
    }
  },
  
  // Helper to add a new notification (for real-time updates)
  addNotification: (notification) => {
    set((state) => ({
      notifications: [notification, ...state.notifications],
      unreadCount: state.unreadCount + 1,
    }));
  },
  
  // Reset state
  reset: () => {
    set({
      notifications: [],
      unreadCount: 0,
      preferences: null,
      loading: false,
      error: null,
      currentPage: 1,
      totalPages: 1,
      filters: {
        type: null,
        is_read: null,
        priority: null,
      },
    });
  },
}));

export default useNotificationStore;

