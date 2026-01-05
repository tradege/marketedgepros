import { Shield, Users, TrendingUp, User, Crown } from 'lucide-react';

/**
 * RoleBadge Component
 * Displays user role with appropriate icon, color, and styling
 */
export default function RoleBadge({ role, size = 'md', showIcon = true, className = '' }) {
  const roleConfig = {
    super_admin: {
      label: 'Super Admin',
      icon: Crown,
      gradient: 'from-purple-500 to-pink-500',
      bg: 'bg-gradient-to-r from-purple-100 to-pink-100',
      text: 'text-purple-700',
      border: 'border-purple-300',
      shadow: 'shadow-purple-200',
      glow: 'shadow-lg shadow-purple-200/50',
    },
    operator: {
      label: 'Operator',
      icon: Shield,
      gradient: 'from-blue-500 to-cyan-500',
      bg: 'bg-gradient-to-r from-blue-100 to-cyan-100',
      text: 'text-blue-700',
      border: 'border-blue-300',
      shadow: 'shadow-blue-200',
      glow: 'shadow-lg shadow-blue-200/50',
    },
    affiliate: {
      label: 'Affiliate',
      icon: TrendingUp,
      gradient: 'from-green-500 to-emerald-500',
      bg: 'bg-gradient-to-r from-green-100 to-emerald-100',
      text: 'text-green-700',
      border: 'border-green-300',
      shadow: 'shadow-green-200',
      glow: 'shadow-lg shadow-green-200/50',
    },
    player: {
      label: 'Player',
      icon: User,
      gradient: 'from-gray-500 to-slate-500',
      bg: 'bg-gradient-to-r from-gray-100 to-slate-100',
      text: 'text-gray-700',
      border: 'border-gray-300',
      shadow: 'shadow-gray-200',
      glow: 'shadow-lg shadow-gray-200/50',
    },
  };

  const config = roleConfig[role] || roleConfig.player;
  const Icon = config.icon;

  const sizeClasses = {
    sm: {
      badge: 'px-2 py-0.5 text-xs',
      icon: 'w-3 h-3',
      gap: 'gap-1',
    },
    md: {
      badge: 'px-3 py-1 text-sm',
      icon: 'w-4 h-4',
      gap: 'gap-1.5',
    },
    lg: {
      badge: 'px-4 py-2 text-base',
      icon: 'w-5 h-5',
      gap: 'gap-2',
    },
  };

  const sizeClass = sizeClasses[size] || sizeClasses.md;

  return (
    <span
      className={`
        inline-flex items-center ${sizeClass.gap} ${sizeClass.badge}
        ${config.bg} ${config.text} ${config.border}
        border rounded-full font-semibold
        transition-all duration-200 hover:${config.glow}
        ${className}
      `}
    >
      {showIcon && <Icon className={sizeClass.icon} />}
      <span>{config.label}</span>
    </span>
  );
}

/**
 * RoleIcon Component
 * Displays just the role icon with background
 */
export function RoleIcon({ role, size = 'md', className = '' }) {
  const roleConfig = {
    super_admin: {
      icon: Crown,
      bg: 'bg-gradient-to-br from-purple-500 to-pink-500',
      text: 'text-white',
    },
    operator: {
      icon: Shield,
      bg: 'bg-gradient-to-br from-blue-500 to-cyan-500',
      text: 'text-white',
    },
    affiliate: {
      icon: TrendingUp,
      bg: 'bg-gradient-to-br from-green-500 to-emerald-500',
      text: 'text-white',
    },
    player: {
      icon: User,
      bg: 'bg-gradient-to-br from-gray-500 to-slate-500',
      text: 'text-white',
    },
  };

  const config = roleConfig[role] || roleConfig.player;
  const Icon = config.icon;

  const sizeClasses = {
    sm: {
      container: 'w-8 h-8',
      icon: 'w-4 h-4',
    },
    md: {
      container: 'w-10 h-10',
      icon: 'w-5 h-5',
    },
    lg: {
      container: 'w-12 h-12',
      icon: 'w-6 h-6',
    },
    xl: {
      container: 'w-16 h-16',
      icon: 'w-8 h-8',
    },
  };

  const sizeClass = sizeClasses[size] || sizeClasses.md;

  return (
    <div
      className={`
        ${sizeClass.container} ${config.bg} ${config.text}
        rounded-full flex items-center justify-center
        shadow-md hover:shadow-lg transition-all duration-200
        ${className}
      `}
    >
      <Icon className={sizeClass.icon} />
    </div>
  );
}

/**
 * RoleHierarchy Component
 * Displays the role hierarchy visually
 */
export function RoleHierarchy({ currentRole, className = '' }) {
  const hierarchy = ['super_admin', 'operator', 'affiliate', 'player'];
  const currentIndex = hierarchy.indexOf(currentRole);

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {hierarchy.map((role, index) => {
        const isActive = index <= currentIndex;
        const isCurrent = role === currentRole;
        
        return (
          <div key={role} className="flex items-center">
            <div className={`
              transition-all duration-200
              ${isActive ? 'opacity-100 scale-100' : 'opacity-30 scale-90'}
              ${isCurrent ? 'ring-2 ring-offset-2 ring-blue-500 rounded-full' : ''}
            `}>
              <RoleIcon role={role} size="sm" />
            </div>
            {index < hierarchy.length - 1 && (
              <div className={`
                w-6 h-0.5 mx-1
                ${isActive ? 'bg-gray-400' : 'bg-gray-200'}
                transition-colors duration-200
              `} />
            )}
          </div>
        );
      })}
    </div>
  );
}

