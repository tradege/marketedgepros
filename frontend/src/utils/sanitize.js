import DOMPurify from 'dompurify';

/**
 * Sanitize HTML content to prevent XSS attacks
 * @param {string} dirty - The HTML string to sanitize
 * @param {object} config - DOMPurify configuration options
 * @returns {string} - Sanitized HTML string
 */
export function sanitizeHTML(dirty, config = {}) {
  const defaultConfig = {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre'],
    ALLOWED_ATTR: ['href', 'target', 'rel', 'class'],
    ALLOW_DATA_ATTR: false,
  };

  const mergedConfig = { ...defaultConfig, ...config };
  return DOMPurify.sanitize(dirty, mergedConfig);
}

/**
 * React component helper for rendering sanitized HTML
 * @param {string} html - The HTML string to sanitize and render
 * @param {object} config - DOMPurify configuration options
 * @returns {object} - Props object for dangerouslySetInnerHTML
 */
export function createSafeHTML(html, config = {}) {
  return {
    __html: sanitizeHTML(html, config)
  };
}

export default { sanitizeHTML, createSafeHTML };
