import { Zap, TrendingUp, Layers, Award, Target, DollarSign } from 'lucide-react';

/**
 * ProgramBadge Component
 * Displays program/challenge type with appropriate styling
 */
export default function ProgramBadge({ type, size = 'md', showIcon = true, className = '' }) {
  const programConfig = {
    instant: {
      label: 'Instant Funding',
      shortLabel: 'Instant',
      icon: Zap,
      gradient: 'from-yellow-500 to-orange-500',
      bg: 'bg-gradient-to-r from-yellow-100 to-orange-100',
      text: 'text-orange-700',
      border: 'border-orange-300',
      glow: 'shadow-lg shadow-orange-200/50',
      description: 'Get funded immediately',
    },
    one_phase: {
      label: 'One Phase Challenge',
      shortLabel: 'One Phase',
      icon: Target,
      gradient: 'from-blue-500 to-indigo-500',
      bg: 'bg-gradient-to-r from-blue-100 to-indigo-100',
      text: 'text-blue-700',
      border: 'border-blue-300',
      glow: 'shadow-lg shadow-blue-200/50',
      description: 'Single evaluation phase',
    },
    two_phase: {
      label: 'Two Phase Challenge',
      shortLabel: 'Two Phase',
      icon: Layers,
      gradient: 'from-purple-500 to-violet-500',
      bg: 'bg-gradient-to-r from-purple-100 to-violet-100',
      text: 'text-purple-700',
      border: 'border-purple-300',
      glow: 'shadow-lg shadow-purple-200/50',
      description: 'Two evaluation phases',
    },
  };

  const config = programConfig[type] || programConfig.two_phase;
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
      <span>{size === 'sm' ? config.shortLabel : config.label}</span>
    </span>
  );
}

/**
 * ProgramCard Component
 * Displays program details in a card format
 */
export function ProgramCard({ program, onClick, className = '' }) {
  const config = {
    instant: {
      icon: Zap,
      gradient: 'from-yellow-500 to-orange-500',
      bgGradient: 'from-yellow-50 to-orange-50',
    },
    one_phase: {
      icon: Target,
      gradient: 'from-blue-500 to-indigo-500',
      bgGradient: 'from-blue-50 to-indigo-50',
    },
    two_phase: {
      icon: Layers,
      gradient: 'from-purple-500 to-violet-500',
      bgGradient: 'from-purple-50 to-violet-50',
    },
  };

  const typeConfig = config[program.type] || config.two_phase;
  const Icon = typeConfig.icon;

  return (
    <div
      onClick={onClick}
      className={`
        relative overflow-hidden rounded-xl border-2 border-gray-200
        bg-gradient-to-br ${typeConfig.bgGradient}
        hover:border-gray-300 hover:shadow-xl
        transition-all duration-300 cursor-pointer
        ${className}
      `}
    >
      {/* Header with gradient */}
      <div className={`
        bg-gradient-to-r ${typeConfig.gradient}
        p-4 text-white
      `}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center">
              <Icon className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-lg">{program.name}</h3>
              <ProgramBadge type={program.type} size="sm" className="mt-1 bg-white/20 border-white/30 text-white" />
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">${program.price}</div>
            <div className="text-xs opacity-90">one-time fee</div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Account Size */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Account Size</span>
          <span className="font-bold text-lg">${(program.account_size / 1000).toFixed(0)}K</span>
        </div>

        {/* Profit Split */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Profit Split</span>
          <span className="font-bold text-green-600">{program.profit_split}%</span>
        </div>

        {/* Targets */}
        {program.type !== 'instant' && (
          <div className="space-y-2 pt-2 border-t border-gray-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Phase 1 Target</span>
              <span className="font-semibold text-blue-600">{program.profit_target_phase1}%</span>
            </div>
            {program.type === 'two_phase' && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Phase 2 Target</span>
                <span className="font-semibold text-purple-600">{program.profit_target_phase2}%</span>
              </div>
            )}
          </div>
        )}

        {/* Risk Limits */}
        <div className="space-y-2 pt-2 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Max Daily Loss</span>
            <span className="font-semibold text-red-600">{program.max_daily_loss}%</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Max Total Loss</span>
            <span className="font-semibold text-red-600">{program.max_total_loss}%</span>
          </div>
        </div>

        {/* Enrollments */}
        {program.enrollments && (
          <div className="pt-2 border-t border-gray-200">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Award className="w-4 h-4" />
              <span>{program.enrollments} traders enrolled</span>
            </div>
          </div>
        )}
      </div>

      {/* Status Indicator */}
      {program.is_active && (
        <div className="absolute top-2 right-2">
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-500 text-white text-xs font-semibold rounded-full">
            <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div>
            Active
          </span>
        </div>
      )}
    </div>
  );
}

/**
 * ProgramTypeSelector Component
 * Allows selecting program type with visual cards
 */
export function ProgramTypeSelector({ selectedType, onChange, className = '' }) {
  const types = [
    {
      value: 'instant',
      label: 'Instant Funding',
      icon: Zap,
      description: 'Get funded immediately without evaluation',
      gradient: 'from-yellow-500 to-orange-500',
      features: ['No evaluation', 'Instant access', 'Higher fees'],
    },
    {
      value: 'one_phase',
      label: 'One Phase',
      icon: Target,
      description: 'Single evaluation phase to prove your skills',
      gradient: 'from-blue-500 to-indigo-500',
      features: ['One evaluation', 'Faster funding', 'Moderate difficulty'],
    },
    {
      value: 'two_phase',
      label: 'Two Phase',
      icon: Layers,
      description: 'Traditional two-phase evaluation process',
      gradient: 'from-purple-500 to-violet-500',
      features: ['Two evaluations', 'Best profit split', 'Standard process'],
    },
  ];

  return (
    <div className={`grid grid-cols-1 md:grid-cols-3 gap-4 ${className}`}>
      {types.map((type) => {
        const Icon = type.icon;
        const isSelected = selectedType === type.value;

        return (
          <button
            key={type.value}
            onClick={() => onChange(type.value)}
            className={`
              relative p-6 rounded-xl border-2 text-left
              transition-all duration-300
              ${isSelected
                ? 'border-blue-500 shadow-lg scale-105'
                : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
              }
            `}
          >
            {/* Icon */}
            <div className={`
              w-12 h-12 rounded-lg flex items-center justify-center mb-4
              bg-gradient-to-r ${type.gradient} text-white
            `}>
              <Icon className="w-6 h-6" />
            </div>

            {/* Label */}
            <h3 className="font-bold text-lg mb-2">{type.label}</h3>
            <p className="text-sm text-gray-600 mb-4">{type.description}</p>

            {/* Features */}
            <ul className="space-y-1">
              {type.features.map((feature, index) => (
                <li key={index} className="text-xs text-gray-500 flex items-center gap-2">
                  <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
                  {feature}
                </li>
              ))}
            </ul>

            {/* Selected Indicator */}
            {isSelected && (
              <div className="absolute top-2 right-2">
                <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
            )}
          </button>
        );
      })}
    </div>
  );
}

