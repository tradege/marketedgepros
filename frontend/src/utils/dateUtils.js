/**
 * Format distance to now (replacement for date-fns formatDistanceToNow)
 * @param {Date} date - The date to format
 * @param {Object} options - Options (addSuffix)
 * @returns {string} Formatted string
 */
export function formatDistanceToNow(date, options = {}) {
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  
  if (diffInSeconds < 60) {
    return options.addSuffix ? 'just now' : 'less than a minute';
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    const text = diffInMinutes === 1 ? '1 minute' : `${diffInMinutes} minutes`;
    return options.addSuffix ? `${text} ago` : text;
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    const text = diffInHours === 1 ? '1 hour' : `${diffInHours} hours`;
    return options.addSuffix ? `${text} ago` : text;
  }
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) {
    const text = diffInDays === 1 ? '1 day' : `${diffInDays} days`;
    return options.addSuffix ? `${text} ago` : text;
  }
  
  const diffInMonths = Math.floor(diffInDays / 30);
  if (diffInMonths < 12) {
    const text = diffInMonths === 1 ? '1 month' : `${diffInMonths} months`;
    return options.addSuffix ? `${text} ago` : text;
  }
  
  const diffInYears = Math.floor(diffInMonths / 12);
  const text = diffInYears === 1 ? '1 year' : `${diffInYears} years`;
  return options.addSuffix ? `${text} ago` : text;
}

/**
 * Format date to locale string
 * @param {Date|string} date - The date to format
 * @param {string} format - Format type ('short', 'long', 'datetime')
 * @returns {string} Formatted date string
 */
export function formatDate(date, format = 'short') {
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (format === 'short') {
    return d.toLocaleDateString();
  } else if (format === 'long') {
    return d.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  } else if (format === 'datetime') {
    return d.toLocaleString();
  }
  
  return d.toLocaleDateString();
}

