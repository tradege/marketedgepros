/**
 * Role Constants - Single Source of Truth
 * All role-related configurations in one place
 */

export const ROLES = {
  SUPERMASTER: 'supermaster',
  SUPER_ADMIN: 'super_admin',
  MASTER: 'master',
  ADMIN: 'admin',
  AGENT: 'agent',
  TRADER: 'trader'
};

/**
 * Role Arrays - Predefined role groups
 * Use these constants instead of hardcoding arrays
 */
export const ADMIN_ROLES = [
  ROLES.SUPERMASTER,
  ROLES.SUPER_ADMIN,
  ROLES.MASTER,
  ROLES.ADMIN
];

export const MANAGEMENT_ROLES = [
  ROLES.SUPERMASTER,
  ROLES.SUPER_ADMIN,
  ROLES.MASTER
];

export const ALL_ROLES = [
  ROLES.SUPERMASTER,
  ROLES.SUPER_ADMIN,
  ROLES.MASTER,
  ROLES.ADMIN,
  ROLES.AGENT,
  ROLES.TRADER
];

export const ROLE_CONFIG = {
  [ROLES.SUPERMASTER]: {
    value: 'supermaster',
    label: 'Super Master',
    color: 'bg-purple-100 text-purple-800',
    darkColor: 'dark:bg-purple-900 dark:text-purple-200',
    hexColor: '#f093fb',
    icon: '👑',
    hierarchy: 1,
    permissions: {
      canCreateUsers: true,
      canCreateWithoutVerification: true,
      canManageCommissions: true,
      canViewAllUsers: true,
      canDeleteUsers: true,
      canManagePrograms: true,
      canManagePayments: true
    }
  },
  [ROLES.SUPER_ADMIN]: {
    value: 'super_admin',
    label: 'Super Admin',
    color: 'bg-purple-100 text-purple-800',
    darkColor: 'dark:bg-purple-900 dark:text-purple-200',
    hexColor: '#f093fb',
    icon: '👑',
    hierarchy: 1,
    permissions: {
      canCreateUsers: true,
      canCreateWithoutVerification: true,
      canManageCommissions: true,
      canViewAllUsers: true,
      canDeleteUsers: true,
      canManagePrograms: true,
      canManagePayments: true
    }
  },
  [ROLES.MASTER]: {
    value: 'master',
    label: 'Master',
    color: 'bg-blue-100 text-blue-800',
    darkColor: 'dark:bg-blue-900 dark:text-blue-200',
    hexColor: '#667eea',
    icon: '⭐',
    hierarchy: 2,
    permissions: {
      canCreateUsers: true,
      canCreateWithoutVerification: false,
      canManageCommissions: false,
      canViewAllUsers: false,
      canDeleteUsers: false,
      canManagePrograms: false,
      canManagePayments: false
    }
  },
  [ROLES.ADMIN]: {
    value: 'admin',
    label: 'Admin',
    color: 'bg-blue-100 text-blue-800',
    darkColor: 'dark:bg-blue-900 dark:text-blue-200',
    hexColor: '#667eea',
    icon: '⭐',
    hierarchy: 2,
    permissions: {
      canCreateUsers: true,
      canCreateWithoutVerification: false,
      canManageCommissions: false,
      canViewAllUsers: false,
      canDeleteUsers: false,
      canManagePrograms: false,
      canManagePayments: false
    }
  },
  [ROLES.AGENT]: {
    value: 'agent',
    label: 'Agent',
    color: 'bg-green-100 text-green-800',
    darkColor: 'dark:bg-green-900 dark:text-green-200',
    hexColor: '#43e97b',
    icon: '🤝',
    hierarchy: 3,
    permissions: {
      canCreateUsers: false,
      canCreateWithoutVerification: false,
      canManageCommissions: false,
      canViewAllUsers: false,
      canDeleteUsers: false,
      canManagePrograms: false,
      canManagePayments: false
    }
  },
  [ROLES.TRADER]: {
    value: 'trader',
    label: 'Trader',
    color: 'bg-gray-100 text-gray-800',
    darkColor: 'dark:bg-gray-700 dark:text-gray-200',
    hexColor: '#94a3b8',
    icon: '📊',
    hierarchy: 4,
    permissions: {
      canCreateUsers: false,
      canCreateWithoutVerification: false,
      canManageCommissions: false,
      canViewAllUsers: false,
      canDeleteUsers: false,
      canManagePrograms: false,
      canManagePayments: false
    }
  }
};

/**
 * Get role configuration by role value
 */
export const getRoleConfig = (role) => {
  return ROLE_CONFIG[role] || ROLE_CONFIG[ROLES.TRADER];
};

/**
 * Get role badge (color + label)
 */
export const getRoleBadge = (role) => {
  const config = getRoleConfig(role);
  return {
    color: config.color,
    label: config.label
  };
};

/**
 * Get role label
 */
export const getRoleLabel = (role) => {
  const config = getRoleConfig(role);
  return config.label;
};

/**
 * Check if role has permission
 */
export const hasPermission = (role, permission) => {
  const config = getRoleConfig(role);
  return config.permissions[permission] || false;
};

/**
 * Get all roles for dropdown
 */
export const getRolesForDropdown = () => {
  return Object.values(ROLE_CONFIG).map(config => ({
    value: config.value,
    label: config.label
  }));
};

/**
 * Get roles that can be created by a specific role
 */
export const getCreatableRoles = (currentRole) => {
  const currentConfig = getRoleConfig(currentRole);
  
  // Only supermaster can create all roles
  if (currentRole === ROLES.SUPERMASTER) {
    return Object.values(ROLE_CONFIG);
  }
  
  // Super Admin can create Master, Admin, Agent, and Trader
  if (currentRole === ROLES.SUPER_ADMIN) {
    return [
      ROLE_CONFIG[ROLES.MASTER],
      ROLE_CONFIG[ROLES.ADMIN],
      ROLE_CONFIG[ROLES.AGENT],
      ROLE_CONFIG[ROLES.TRADER]
    ];
  }
  
  // Master/Admin can create Agent and Trader
  if (currentRole === ROLES.MASTER || currentRole === ROLES.ADMIN) {
    return [ROLE_CONFIG[ROLES.AGENT], ROLE_CONFIG[ROLES.TRADER]];
  }
  
  // Others cannot create users
  return [];
};



/**
 * Get role hex color (for gradients, charts, etc.)
 */
export const getRoleColor = (role) => {
  const config = getRoleConfig(role);
  return config.hexColor || '#94a3b8';
};

