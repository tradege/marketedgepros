import { CheckCircle, XCircle, Clock, Trophy, TrendingUp, AlertCircle } from 'lucide-react';

/**
 * ChallengeStatusBadge Component
 * Displays challenge status with appropriate styling
 */
export default function ChallengeStatusBadge({ status, size = 'md', showIcon = true, className = '' }) {
  const statusConfig = {
    active: {
      label: 'Active',
      icon: Clock,
      gradient: 'from-blue-500 to-cyan-500',
      bg: 'bg-gradient-to-r from-blue-100 to-cyan-100',
      text: 'text-blue-700',
      border: 'border-blue-300',
      glow: 'shadow-lg shadow-blue-200/50',
      pulse: true,
    },
    passed: {
      label: 'Passed',
      icon: CheckCircle,
      gradient: 'from-green-500 to-emerald-500',
      bg: 'bg-gradient-to-r from-green-100 to-emerald-100',
      text: 'text-green-700',
      border: 'border-green-300',
      glow: 'shadow-lg shadow-green-200/50',
      pulse: false,
    },
    failed: {
      label: 'Failed',
      icon: XCircle,
      gradient: 'from-red-500 to-rose-500',
      bg: 'bg-gradient-to-r from-red-100 to-rose-100',
      text: 'text-red-700',
      border: 'border-red-300',
      glow: 'shadow-lg shadow-red-200/50',
      pulse: false,
    },
    funded: {
      label: 'Funded',
      icon: Trophy,
      gradient: 'from-yellow-500 to-orange-500',
      bg: 'bg-gradient-to-r from-yellow-100 to-orange-100',
      text: 'text-orange-700',
      border: 'border-orange-300',
      glow: 'shadow-lg shadow-orange-200/50',
      pulse: false,
    },
    pending: {
      label: 'Pending',
      icon: AlertCircle,
      gradient: 'from-gray-500 to-slate-500',
      bg: 'bg-gradient-to-r from-gray-100 to-slate-100',
      text: 'text-gray-700',
      border: 'border-gray-300',
      glow: 'shadow-lg shadow-gray-200/50',
      pulse: false,
    },
  };

  const config = statusConfig[status] || statusConfig.pending;
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
      {showIcon && (
        <Icon className={`${sizeClass.icon} ${config.pulse ? 'animate-pulse' : ''}`} />
      )}
      <span>{config.label}</span>
    </span>
  );
}

/**
 * ChallengeProgressBar Component
 * Shows progress towards profit target
 */
export function ChallengeProgressBar({ 
  current, 
  target, 
  type = 'profit', 
  className = '' 
}) {
  const percentage = Math.min((current / target) * 100, 100);
  const isComplete = percentage >= 100;
  const isWarning = percentage > 80 && percentage < 100;

  const colors = {
    profit: {
      bg: 'bg-green-100',
      fill: isComplete ? 'bg-green-500' : isWarning ? 'bg-yellow-500' : 'bg-green-400',
      text: 'text-green-700',
    },
    loss: {
      bg: 'bg-red-100',
      fill: isComplete ? 'bg-red-600' : isWarning ? 'bg-orange-500' : 'bg-red-400',
      text: 'text-red-700',
    },
    days: {
      bg: 'bg-blue-100',
      fill: isComplete ? 'bg-blue-500' : isWarning ? 'bg-blue-400' : 'bg-blue-300',
      text: 'text-blue-700',
    },
  };

  const color = colors[type] || colors.profit;

  return (
    <div className={`space-y-2 ${className}`}>
      <div className="flex items-center justify-between text-sm">
        <span className={`font-medium ${color.text}`}>
          {type === 'profit' ? 'Profit' : type === 'loss' ? 'Loss' : 'Trading Days'}
        </span>
        <span className={`font-bold ${color.text}`}>
          {current.toFixed(2)}{type !== 'days' ? '%' : ''} / {target}{type !== 'days' ? '%' : ''}
        </span>
      </div>
      <div className={`relative h-3 ${color.bg} rounded-full overflow-hidden`}>
        <div
          className={`absolute top-0 left-0 h-full ${color.fill} transition-all duration-500 ease-out rounded-full`}
          style={{ width: `${percentage}%` }}
        >
          {isComplete && (
            <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
          )}
        </div>
      </div>
      <div className="text-xs text-gray-500 text-right">
        {percentage.toFixed(1)}% complete
      </div>
    </div>
  );
}

/**
 * ChallengePhaseIndicator Component
 * Shows current phase in multi-phase challenges
 */
export function ChallengePhaseIndicator({ currentPhase, totalPhases, className = '' }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {Array.from({ length: totalPhases }, (_, i) => {
        const phaseNum = i + 1;
        const isActive = phaseNum === currentPhase;
        const isComplete = phaseNum < currentPhase;

        return (
          <div key={phaseNum} className="flex items-center">
            <div
              className={`
                w-10 h-10 rounded-full flex items-center justify-center
                font-bold text-sm transition-all duration-300
                ${isComplete
                  ? 'bg-green-500 text-white'
                  : isActive
                  ? 'bg-blue-500 text-white ring-4 ring-blue-200'
                  : 'bg-gray-200 text-gray-500'
                }
              `}
            >
              {isComplete ? (
                <CheckCircle className="w-5 h-5" />
              ) : (
                phaseNum
              )}
            </div>
            {phaseNum < totalPhases && (
              <div
                className={`
                  w-8 h-1 mx-1
                  ${isComplete ? 'bg-green-500' : 'bg-gray-200'}
                  transition-colors duration-300
                `}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

/**
 * ChallengeMetrics Component
 * Displays key challenge metrics in a grid
 */
export function ChallengeMetrics({ metrics, className = '' }) {
  const metricItems = [
    {
      label: 'Current Balance',
      value: `$${metrics.balance?.toLocaleString() || '0'}`,
      icon: TrendingUp,
      color: 'blue',
    },
    {
      label: 'Total Profit',
      value: `${metrics.profit >= 0 ? '+' : ''}${metrics.profit?.toFixed(2) || '0'}%`,
      icon: TrendingUp,
      color: metrics.profit >= 0 ? 'green' : 'red',
    },
    {
      label: 'Daily Loss',
      value: `${metrics.dailyLoss?.toFixed(2) || '0'}%`,
      icon: AlertCircle,
      color: metrics.dailyLoss > 3 ? 'red' : 'gray',
    },
    {
      label: 'Trading Days',
      value: `${metrics.tradingDays || 0} / ${metrics.minTradingDays || 0}`,
      icon: Clock,
      color: 'blue',
    },
  ];

  return (
    <div className={`grid grid-cols-2 md:grid-cols-4 gap-4 ${className}`}>
      {metricItems.map((item, index) => {
        const Icon = item.icon;
        const colorClasses = {
          blue: 'bg-blue-50 text-blue-700 border-blue-200',
          green: 'bg-green-50 text-green-700 border-green-200',
          red: 'bg-red-50 text-red-700 border-red-200',
          gray: 'bg-gray-50 text-gray-700 border-gray-200',
        };

        return (
          <div
            key={index}
            className={`
              p-4 rounded-lg border-2
              ${colorClasses[item.color]}
              transition-all duration-200 hover:shadow-md
            `}
          >
            <div className="flex items-center gap-2 mb-2">
              <Icon className="w-4 h-4" />
              <span className="text-xs font-medium opacity-75">{item.label}</span>
            </div>
            <div className="text-2xl font-bold">{item.value}</div>
          </div>
        );
      })}
    </div>
  );
}

/**
 * ChallengeSummaryCard Component
 * Complete challenge overview card
 */
export function ChallengeSummaryCard({ challenge, onClick, className = '' }) {
  return (
    <div
      onClick={onClick}
      className={`
        bg-white rounded-xl border-2 border-gray-200 p-6
        hover:border-blue-300 hover:shadow-lg
        transition-all duration-300 cursor-pointer
        ${className}
      `}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-bold text-lg mb-2">{challenge.program_name}</h3>
          <div className="flex items-center gap-2">
            <ChallengeStatusBadge status={challenge.status} size="sm" />
            {challenge.total_phases > 1 && (
              <span className="text-xs text-gray-500">
                Phase {challenge.current_phase} of {challenge.total_phases}
              </span>
            )}
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-gray-900">
            ${(challenge.account_size / 1000).toFixed(0)}K
          </div>
          <div className="text-xs text-gray-500">Account Size</div>
        </div>
      </div>

      {/* Phase Indicator */}
      {challenge.total_phases > 1 && (
        <div className="mb-4">
          <ChallengePhaseIndicator
            currentPhase={challenge.current_phase}
            totalPhases={challenge.total_phases}
          />
        </div>
      )}

      {/* Progress Bars */}
      <div className="space-y-3 mb-4">
        <ChallengeProgressBar
          current={challenge.current_profit || 0}
          target={challenge.profit_target}
          type="profit"
        />
        {challenge.trading_days !== undefined && (
          <ChallengeProgressBar
            current={challenge.trading_days}
            target={challenge.min_trading_days}
            type="days"
          />
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <span className="text-sm text-gray-600">
          Started {new Date(challenge.created_at).toLocaleDateString()}
        </span>
        <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
          View Details →
        </button>
      </div>
    </div>
  );
}

