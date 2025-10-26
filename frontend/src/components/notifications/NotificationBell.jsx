import { useState, useEffect, useRef } from 'react';
import { Bell } from 'lucide-react';
import useNotificationStore from '../../stores/notificationStore';
import NotificationDropdown from './NotificationDropdown';

export default function NotificationBell() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const buttonRef = useRef(null);
  const { unreadCount, fetchUnreadCount } = useNotificationStore();
  
  // Poll for unread count every 30 seconds
  useEffect(() => {
    fetchUnreadCount();
    const interval = setInterval(() => {
      fetchUnreadCount();
    }, 30000); // 30 seconds
    
    return () => clearInterval(interval);
  }, [fetchUnreadCount]);
  
  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (
        dropdownRef.current && 
        !dropdownRef.current.contains(event.target) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);
  
  const handleClick = () => {
    setIsOpen(!isOpen);
  };
  
  const handleClose = () => {
    setIsOpen(false);
  };
  
  return (
    <div className="relative">
      <button
        ref={buttonRef}
        onClick={handleClick}
        className="relative p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
        aria-label="notifications"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 flex items-center justify-center min-w-[18px] h-[18px] px-1 text-xs font-bold text-white bg-red-500 rounded-full">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>
      
      {isOpen && (
        <div
          ref={dropdownRef}
          className="absolute right-0 mt-2 w-96 max-h-[600px] bg-slate-800 border border-white/10 rounded-lg shadow-xl z-50"
        >
          <NotificationDropdown onClose={handleClose} />
        </div>
      )}
    </div>
  );
}

