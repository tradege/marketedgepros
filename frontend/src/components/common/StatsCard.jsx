export default function StatsCard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  color = 'primary',
  trend,
  trendValue 
}) {
  const colors = {
    primary: 'from-purple-600 to-purple-800',
    success: 'from-green-600 to-green-800',
    warning: 'from-yellow-600 to-yellow-800',
    error: 'from-red-600 to-red-800',
    info: 'from-cyan-600 to-cyan-800',
  };

  const iconBgColors = {
    primary: 'bg-gradient-to-br from-purple-600 to-purple-800',
    success: 'bg-gradient-to-br from-green-600 to-green-800',
    warning: 'bg-gradient-to-br from-yellow-600 to-yellow-800',
    error: 'bg-gradient-to-br from-red-600 to-red-800',
    info: 'bg-gradient-to-br from-cyan-600 to-cyan-800',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            {title}
          </p>
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-1">
            {value}
          </h3>
          {subtitle && (
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {subtitle}
            </p>
          )}
          {trend && (
            <div className="flex items-center mt-2">
              <span className={`text-sm font-semibold ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                {trend === 'up' ? '↑' : '↓'} {trendValue}
              </span>
              <span className="text-sm text-gray-600 dark:text-gray-400 ml-1">
                this month
              </span>
            </div>
          )}
        </div>
        <div className={`w-14 h-14 rounded-lg ${iconBgColors[color]} flex items-center justify-center shadow-lg`}>
          {Icon && <Icon className="text-white" style={{ fontSize: 28 }} />}
        </div>
      </div>
    </div>
  );
}

