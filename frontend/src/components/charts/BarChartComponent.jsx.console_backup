import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const BarChartComponent = ({ 
  data, 
  title, 
  dataKeys, 
  colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042'],
  height = 300,
  xAxisKey = 'name',
  yAxisLabel = '',
  layout = 'vertical'
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
            {title}
          </h2>
          <div className="flex items-center justify-center" style={{ height }}>
            <p className="text-gray-500 dark:text-gray-400">No data available</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
          {title}
        </h2>
        <ResponsiveContainer width="100%" height={height}>
          <BarChart
            data={data}
            layout={layout}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            {layout === 'vertical' ? (
              <>
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis 
                  type="category" 
                  dataKey={xAxisKey}
                  tick={{ fontSize: 12 }}
                  width={100}
                />
              </>
            ) : (
              <>
                <XAxis 
                  dataKey={xAxisKey}
                  tick={{ fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis 
                  label={{ value: yAxisLabel, angle: -90, position: 'insideLeft' }}
                  tick={{ fontSize: 12 }}
                />
              </>
            )}
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            />
            <Legend />
            {dataKeys.map((key, index) => (
              <Bar
                key={key.key}
                dataKey={key.key}
                name={key.name}
                fill={colors[index % colors.length]}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BarChartComponent;