import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

/**
 * Professional Dashboard Card Component
 * Following Material Design 3 guidelines
 */
export default function DashboardCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendValue,
  color = 'cyan',
  onClick,
  loading = false,
}) {
  const colorClasses = {
    cyan: {
      gradient: 'from-cyan-500 to-teal-500',
      bg: 'bg-cyan-500/10',
      border: 'border-cyan-500/30',
      text: 'text-cyan-400',
      shadow: 'hover:shadow-cyan-500/20',
    },
    purple: {
      gradient: 'from-purple-500 to-pink-500',
      bg: 'bg-purple-500/10',
      border: 'border-purple-500/30',
      text: 'text-purple-400',
      shadow: 'hover:shadow-purple-500/20',
    },
    green: {
      gradient: 'from-green-500 to-emerald-500',
      bg: 'bg-green-500/10',
      border: 'border-green-500/30',
      text: 'text-green-400',
      shadow: 'hover:shadow-green-500/20',
    },
    amber: {
      gradient: 'from-amber-500 to-orange-500',
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/30',
      text: 'text-amber-400',
      shadow: 'hover:shadow-amber-500/20',
    },
    blue: {
      gradient: 'from-blue-500 to-indigo-500',
      bg: 'bg-blue-500/10',
      border: 'border-blue-500/30',
      text: 'text-blue-400',
      shadow: 'hover:shadow-blue-500/20',
    },
    red: {
      gradient: 'from-red-500 to-rose-500',
      bg: 'bg-red-500/10',
      border: 'border-red-500/30',
      text: 'text-red-400',
      shadow: 'hover:shadow-red-500/20',
    },
  };

  const colors = colorClasses[color] || colorClasses.cyan;

  const getTrendIcon = () => {
    if (trend === 'up') return <TrendingUp className="w-4 h-4" />;
    if (trend === 'down') return <TrendingDown className="w-4 h-4" />;
    return <Minus className="w-4 h-4" />;
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-green-400';
    if (trend === 'down') return 'text-red-400';
    return 'text-gray-400';
  };

  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-2xl p-6 animate-pulse">
        <div className="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
        <div className="h-8 bg-slate-700 rounded w-3/4 mb-2"></div>
        <div className="h-3 bg-slate-700 rounded w-1/3"></div>
      </div>
    );
  }

  return (
    <div
      onClick={onClick}
      className={`
        group relative bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-2xl p-6
        transition-all duration-300 hover:bg-slate-800/70 hover:border-white/20
        ${onClick ? 'cursor-pointer hover:scale-105' : ''}
        ${colors.shadow} hover:shadow-xl
      `}
    >
      {/* Icon Badge */}
      <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl ${colors.bg} border ${colors.border} mb-4`}>
        {Icon && <Icon className={`w-6 h-6 ${colors.text}`} />}
      </div>

      {/* Title */}
      <h3 className="text-sm font-medium text-gray-400 mb-2">{title}</h3>

      {/* Value */}
      <div className="flex items-baseline gap-3 mb-2">
        <p className={`text-3xl font-bold bg-gradient-to-r ${colors.gradient} bg-clip-text text-transparent`}>
          {value}
        </p>
        
        {/* Trend */}
        {trendValue && (
          <div className={`flex items-center gap-1 text-sm font-semibold ${getTrendColor()}`}>
            {getTrendIcon()}
            <span>{trendValue}</span>
          </div>
        )}
      </div>

      {/* Subtitle */}
      {subtitle && (
        <p className="text-sm text-gray-400">{subtitle}</p>
      )}

      {/* Hover Effect Gradient */}
      <div className={`absolute inset-0 bg-gradient-to-br ${colors.gradient} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity duration-300`}></div>
    </div>
  );
}

