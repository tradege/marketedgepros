import React, { useState, useEffect } from 'react';
import { Loader2, AlertCircle } from 'lucide-react';
import axios from 'axios';
import LineChartComponent from '../../components/charts/LineChartComponent';
import BarChartComponent from '../../components/charts/BarChartComponent';
import PieChartComponent from '../../components/charts/PieChartComponent';
import AdminLayout from '../../components/admin/AdminLayout';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const AnalyticsDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState(30);
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        `${API_BASE_URL}/analytics/comprehensive?days=${timeRange}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setAnalyticsData(response.data.data);
    } catch (err) {
      setError('Failed to load analytics data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTimeRangeChange = (event) => {
    setTimeRange(event.target.value);
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-8 mb-8">
        <div className="flex justify-center items-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-gray-600 dark:text-gray-300" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-8 mb-8">
        <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-500/40 dark:bg-red-500/10 dark:text-red-200">
          <AlertCircle className="h-5 w-5 mt-0.5 shrink-0" />
          <div className="text-sm">{error}</div>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return null;
  }

  // Prepare data for charts
  const revenueData = analyticsData.revenue_over_time || [];
  const userGrowthData = analyticsData.user_growth || [];
  const challengeStats = analyticsData.challenge_statistics || {};
  const kycStats = analyticsData.kyc_statistics || {};
  const referralStats = analyticsData.referral_statistics || {};
  const paymentStats = analyticsData.payment_statistics || {};

  // Transform challenge status distribution for pie chart
  const challengeStatusData = (challengeStats.status_distribution || []).map(item => ({
    name: item.status.charAt(0).toUpperCase() + item.status.slice(1),
    value: item.count
  }));

  // Transform KYC distribution for pie chart
  const kycDistributionData = (kycStats.distribution || []).map(item => ({
    name: item.status.charAt(0).toUpperCase() + item.status.slice(1).replace('_', ' '),
    value: item.count
  }));

  // Transform payment method distribution for bar chart
  const paymentMethodData = (paymentStats.method_distribution || []).map(item => ({
    name: item.method.charAt(0).toUpperCase() + item.method.slice(1),
    count: item.count,
    amount: item.total_amount
  }));

  return (
    <AdminLayout>
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-8 mb-8">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-6">
        <h1 className="text-2xl sm:text-3xl font-semibold text-gray-900 dark:text-gray-100">
          Analytics Dashboard
        </h1>
        <div className="w-full sm:w-auto">
          <label htmlFor="timeRange" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
            Time Range
          </label>
          <select
            id="timeRange"
            value={timeRange}
            onChange={handleTimeRangeChange}
            className="block w-full sm:min-w-[200px] rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm outline-none transition focus:border-gray-900 focus:ring-2 focus:ring-gray-900/10 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 dark:focus:border-gray-100 dark:focus:ring-gray-100/10"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={180}>Last 6 months</option>
            <option value={365}>Last year</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Revenue Over Time */}
        <div className="col-span-12 lg:col-span-6">
          <LineChartComponent
            data={revenueData}
            title="Revenue Over Time"
            dataKeys={[
              { key: 'revenue', name: 'Revenue ($)' },
              { key: 'transactions', name: 'Transactions' }
            ]}
            colors={['#00C49F', '#8884D8']}
            height={350}
            yAxisLabel="Amount ($)"
          />
        </div>

        {/* User Growth */}
        <div className="col-span-12 lg:col-span-6">
          <LineChartComponent
            data={userGrowthData}
            title="User Growth"
            dataKeys={[
              { key: 'registrations', name: 'New Users' },
              { key: 'cumulative', name: 'Total Users' }
            ]}
            colors={['#0088FE', '#FFBB28']}
            height={350}
            yAxisLabel="Users"
          />
        </div>

        {/* Challenge Status Distribution */}
        <div className="col-span-12 md:col-span-6 lg:col-span-4">
          <PieChartComponent
            data={challengeStatusData}
            title="Challenge Status Distribution"
            dataKey="value"
            nameKey="name"
            height={300}
          />
        </div>

        {/* KYC Status Distribution */}
        <div className="col-span-12 md:col-span-6 lg:col-span-4">
          <PieChartComponent
            data={kycDistributionData}
            title="KYC Status Distribution"
            dataKey="value"
            nameKey="name"
            height={300}
          />
        </div>

        {/* Payment Methods */}
        <div className="col-span-12 md:col-span-12 lg:col-span-4">
          <BarChartComponent
            data={paymentMethodData}
            title="Payment Methods"
            dataKeys={[
              { key: 'count', name: 'Transactions' }
            ]}
            colors={['#8884D8']}
            height={300}
            xAxisKey="name"
            layout="vertical"
          />
        </div>

        {/* Challenge Daily Statistics */}
        {challengeStats.daily_data && challengeStats.daily_data.length > 0 && (
          <div className="col-span-12">
            <LineChartComponent
              data={challengeStats.daily_data}
              title="Challenge Activity"
              dataKeys={[
                { key: 'created', name: 'Created' },
                { key: 'completed', name: 'Completed' },
                { key: 'funded', name: 'Funded' }
              ]}
              colors={['#8884D8', '#00C49F', '#FFBB28']}
              height={350}
              yAxisLabel="Challenges"
            />
          </div>
        )}

        {/* Top Performing Agents */}
        {referralStats.top_agents && referralStats.top_agents.length > 0 && (
          <div className="col-span-12">
            <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-950">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
                Top Performing Agents
              </h2>
              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b-2 border-gray-200 dark:border-gray-800">
                      <th className="py-3 px-3 text-left text-sm font-medium text-gray-600 dark:text-gray-300">Name</th>
                      <th className="py-3 px-3 text-left text-sm font-medium text-gray-600 dark:text-gray-300">Email</th>
                      <th className="py-3 px-3 text-right text-sm font-medium text-gray-600 dark:text-gray-300">Referrals</th>
                      <th className="py-3 px-3 text-right text-sm font-medium text-gray-600 dark:text-gray-300">Total Commission</th>
                    </tr>
                  </thead>
                  <tbody>
                    {referralStats.top_agents.map((agent) => (
                      <tr key={agent.agent_id} className="border-b border-gray-100 dark:border-gray-800">
                        <td className="py-3 px-3 text-sm text-gray-900 dark:text-gray-100">{agent.name}</td>
                        <td className="py-3 px-3 text-sm text-gray-900 dark:text-gray-100">{agent.email}</td>
                        <td className="py-3 px-3 text-sm text-right text-gray-900 dark:text-gray-100">{agent.referrals}</td>
                        <td className="py-3 px-3 text-sm text-right text-gray-900 dark:text-gray-100">
                          ${agent.total_commission.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Referral Statistics Summary */}
        <div className="col-span-12 md:col-span-4">
          <div className="h-full rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-950">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Referral Statistics
            </h2>
            <div className="mt-2">
              <div className="text-xs font-medium text-gray-600 dark:text-gray-400">
                Total Referrals
              </div>
              <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                {referralStats.total_referrals || 0}
              </div>
            </div>
            <div className="mt-4">
              <div className="text-xs font-medium text-gray-600 dark:text-gray-400">
                Active Referrals
              </div>
              <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                {referralStats.active_referrals || 0}
              </div>
            </div>
            <div className="mt-4">
              <div className="text-xs font-medium text-gray-600 dark:text-gray-400">
                Conversion Rate
              </div>
              <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                {referralStats.conversion_rate || 0}%
              </div>
            </div>
          </div>
        </div>

        {/* Payment Statistics Summary */}
        <div className="col-span-12 md:col-span-8">
          <div className="h-full rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-950">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Payment Status Distribution
            </h2>
            <div className="mt-4 flex flex-wrap gap-6">
              {(paymentStats.status_distribution || []).map((item) => (
                <div key={item.status} className="min-w-[150px]">
                  <div className="text-xs font-medium text-gray-600 dark:text-gray-400">
                    {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                  </div>
                  <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                    {item.count}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
    </AdminLayout>
  );
};

export default AnalyticsDashboard;