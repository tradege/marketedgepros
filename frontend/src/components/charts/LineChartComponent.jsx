import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const LineChartComponent = ({ 
  data, 
  title, 
  dataKeys, 
  colors = ['#8884d8', '#82ca9d', '#ffc658'],
  height = 300,
  xAxisKey = 'date',
  yAxisLabel = ''
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <div className="p-4 sm:p-6">
          <div className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            {title}
          </div>
          <div
            className="flex items-center justify-center"
            style={{ height }}
          >
            <div className="text-gray-500 dark:text-gray-400">
              No data available
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <div className="p-4 sm:p-6">
        <div className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
          {title}
        </div>
        <ResponsiveContainer width="100%" height={height}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
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
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            />
            <Legend />
            {dataKeys.map((key, index) => (
              <Line
                key={key.key}
                type="monotone"
                dataKey={key.key}
                name={key.name}
                stroke={colors[index % colors.length]}
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LineChartComponent;