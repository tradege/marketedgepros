import { create } from 'zustand';
import { authAPI } from '../services/api';

const INACTIVITY_TIMEOUT = 15 * 60 * 1000; // 15 minutes in milliseconds

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  lastActivity: Date.now(),
  inactivityTimer: null,

  // Update last activity timestamp
  updateActivity: () => {
    const state = get();
    set({ lastActivity: Date.now() });
    
    // Clear existing timer
    if (state.inactivityTimer) {
      clearTimeout(state.inactivityTimer);
    }
    
    // Set new timer
    const timer = setTimeout(() => {
      const { isAuthenticated, logout } = get();
      if (isAuthenticated) {
        logout();
      }
    }, INACTIVITY_TIMEOUT);
    
    set({ inactivityTimer: timer });
  },

  // Initialize auth state from localStorage
  init: async () => {
    const token = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');
    
    if (token) {
      try {
        // Try to get fresh user data from API
        const response = await authAPI.getCurrentUser();
        const user = response.data.user;
        
        // Update localStorage with fresh data
        localStorage.setItem('user', JSON.stringify(user));
        
        set({
          user: user,
          isAuthenticated: true,
          isLoading: false,
        });
        
        // Start inactivity tracking
        get().updateActivity();
        
        // Track user activity
        const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
        events.forEach(event => {
          document.addEventListener(event, get().updateActivity);
        });
      } catch (error) {
        // If API fails but we have stored user, use it as fallback
        if (storedUser) {
          try {
            const user = JSON.parse(storedUser);
            set({
              user: user,
              isAuthenticated: true,
              isLoading: false,
            });
            
            // Start inactivity tracking
            get().updateActivity();
            
            // Track user activity
            const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
            events.forEach(event => {
              document.addEventListener(event, get().updateActivity);
            });
          } catch (parseError) {
            // If parsing fails, clear everything
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            set({ isLoading: false });
          }
        } else {
          // No stored user, clear tokens
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          set({ isLoading: false });
        }
      }
    } else {
      set({ isLoading: false });
    }
  },

  // Login
  login: async (email, password) => {
    try {
      set({ error: null });
      const response = await authAPI.login({ email, password });

      // Check if 2FA is required
      if (response.data.requires_2fa) {
        return { requires2FA: true, userId: response.data.user_id };
      }

      // Save tokens and user
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      set({
        user: response.data.user,
        isAuthenticated: true,
      });
      
      // Start inactivity tracking
      get().updateActivity();
      
      // Track user activity
      const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
      events.forEach(event => {
        document.addEventListener(event, get().updateActivity);
      });

      return { success: true, user: response.data.user };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Login failed';
      set({ error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  // Login with 2FA
  login2FA: async (userId, token) => {
    try {
      set({ error: null });
      const response = await authAPI.login2FA({ user_id: userId, token });

      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      set({
        user: response.data.user,
        isAuthenticated: true,
      });
      
      // Start inactivity tracking
      get().updateActivity();
      
      // Track user activity
      const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
      events.forEach(event => {
        document.addEventListener(event, get().updateActivity);
      });

      return { success: true, user: response.data.user };
    } catch (error) {
      const errorMessage = error.response?.data?.error || '2FA verification failed';
      set({ error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  // Register
  register: async (data) => {
    try {
      set({ error: null });
      const response = await authAPI.register(data);
      return { success: true, user: response.data.user };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Registration failed';
      set({ error: errorMessage });
      throw new Error(errorMessage);
    }
  },

  // Logout
  logout: async () => {
    try {
      await authAPI.logout();
    } catch (error) {
    } finally {
      // Clear inactivity timer
      const state = get();
      if (state.inactivityTimer) {
        clearTimeout(state.inactivityTimer);
      }
      
      // Remove event listeners
      const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
      events.forEach(event => {
        document.removeEventListener(event, get().updateActivity);
      });
      
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      set({
        user: null,
        isAuthenticated: false,
        inactivityTimer: null,
      });
    }
  },

  // Update user
  updateUser: (userData) => {
    set({ user: userData });
  },

  // Clear error
  clearError: () => {
    set({ error: null });
  },
}));

export default useAuthStore;

