/**
 * Role color mappings for UI components
 */

export const getRoleColor = (role) => {
  const colorMap = {
    'supermaster': '#f093fb',
    'super_admin': '#f093fb',
    'master': '#667eea',
    'admin': '#667eea',
    'agent': '#43e97b',
    'trader': '#94a3b8',
    'guest': '#94a3b8',
  };
  
  return colorMap[role] || '#94a3b8';
};

