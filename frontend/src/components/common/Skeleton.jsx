// Skeleton loading components for better UX

export const Skeleton = ({ className = '', variant = 'default' }) => {
  const baseClasses = 'animate-pulse bg-slate-700/50 rounded';
  
  const variantClasses = {
    default: 'h-4',
    text: 'h-4',
    title: 'h-8',
    button: 'h-10',
    avatar: 'h-12 w-12 rounded-full',
    card: 'h-32',
    input: 'h-10',
  };

  return (
    <div className={`${baseClasses} ${variantClasses[variant]} ${className}`} />
  );
};

export const SkeletonCard = () => {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 space-y-4">
      <div className="flex items-center justify-between">
        <Skeleton className="w-32" variant="text" />
        <Skeleton className="w-12 h-12 rounded-lg" />
      </div>
      <Skeleton className="w-24" variant="title" />
      <Skeleton className="w-20" variant="text" />
    </div>
  );
};

export const SkeletonTable = ({ rows = 5, columns = 4 }) => {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="border-b border-slate-700 p-4">
        <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
          {Array.from({ length: columns }).map((_, i) => (
            <Skeleton key={i} className="w-24" variant="text" />
          ))}
        </div>
      </div>
      
      {/* Rows */}
      <div className="divide-y divide-slate-700">
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="p-4">
            <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
              {Array.from({ length: columns }).map((_, colIndex) => (
                <Skeleton key={colIndex} className="w-full" variant="text" />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const SkeletonDashboard = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>

      {/* Charts/Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 space-y-4">
          <Skeleton className="w-40" variant="title" />
          <Skeleton className="w-full h-64" />
        </div>
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 space-y-4">
          <Skeleton className="w-40" variant="title" />
          <Skeleton className="w-full h-64" />
        </div>
      </div>
    </div>
  );
};

export const SkeletonList = ({ items = 5 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 p-3 bg-slate-800 rounded-lg border border-slate-700">
          <Skeleton variant="avatar" />
          <div className="flex-1 space-y-2">
            <Skeleton className="w-32" variant="text" />
            <Skeleton className="w-48" variant="text" />
          </div>
          <Skeleton className="w-20" variant="button" />
        </div>
      ))}
    </div>
  );
};

export const SkeletonForm = () => {
  return (
    <div className="space-y-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="space-y-2">
          <Skeleton className="w-24" variant="text" />
          <Skeleton className="w-full" variant="input" />
        </div>
      ))}
      <Skeleton className="w-32" variant="button" />
    </div>
  );
};

