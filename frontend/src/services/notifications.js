// Simple notification service
// Can be replaced with toast library like react-toastify or react-hot-toast

class NotificationService {
  constructor() {
    this.listeners = [];
  }

  subscribe(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }

  notify(message, type = 'info', duration = 3000) {
    const notification = {
      id: Date.now() + Math.random(),
      message,
      type, // 'success', 'error', 'warning', 'info'
      duration,
      timestamp: new Date(),
    };

    this.listeners.forEach(listener => listener(notification));
  }

  success(message, duration) {
    this.notify(message, 'success', duration);
  }

  error(message, duration) {
    this.notify(message, 'error', duration);
  }

  warning(message, duration) {
    this.notify(message, 'warning', duration);
  }

  info(message, duration) {
    this.notify(message, 'info', duration);
  }
}

export const notificationService = new NotificationService();

export default notificationService;

