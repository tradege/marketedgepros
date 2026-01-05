import { useState, useEffect } from 'react';
import { TrendingUp, DollarSign, Trophy, Clock } from 'lucide-react';
import StatsCard from '../../components/common/StatsCard';
import api from '../../services/api';
import UserLayout from '../../components/layout/UserLayout';

export default function UserDashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/users/dashboard');
      setDashboardData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mb-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return null;
  }

  const { user, statistics, recent_challenges } = dashboardData;

  const userStats = [
    { 
      title: 'Active Challenges', 
      value: statistics.active_challenges.toString(), 
      subtitle: 'In progress', 
      icon: Clock, 
      color: 'primary' 
    },
    { 
      title: 'Total Profit', 
      value: `$${statistics.total_profit.toLocaleString()}`, 
      subtitle: `${statistics.funded_challenges} funded account${statistics.funded_challenges !== 1 ? 's' : ''}`, 
      icon: DollarSign, 
      color: 'success',
      trend: statistics.total_profit > 0 ? 'up' : undefined,
      trendValue: statistics.total_profit > 0 ? `+$${statistics.total_profit.toLocaleString()}` : undefined
    },
    { 
      title: 'Success Rate', 
      value: `${statistics.success_rate}%`, 
      subtitle: `${statistics.passed_challenges} passed / ${statistics.failed_challenges} failed`, 
      icon: TrendingUp, 
      color: 'info' 
    },
    { 
      title: 'Funded Accounts', 
      value: statistics.funded_challenges.toString(), 
      subtitle: statistics.funded_challenges > 0 ? 'Congratulations!' : 'Keep trading!', 
      icon: Trophy, 
      color: 'warning' 
    },
  ];

  const calculateProgress = (challenge) => {
    if (!challenge.initial_balance || !challenge.current_balance) return 0;
    const profit = challenge.profit;
    const target = challenge.initial_balance * 0.08;
    const progress = (profit / target) * 100;
    return Math.min(Math.max(progress, 0), 100);
  };

  const getStatusColor = (status) => {
    const statusLower = status?.toLowerCase();
    if (statusLower === 'active') return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    if (statusLower === 'passed') return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
    if (statusLower === 'failed') return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    if (statusLower === 'funded') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
    if (statusLower === 'pending') return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
    return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
  };

  return (
    <UserLayout>
      <div>
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back, {user.first_name}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Here's your trading overview
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          {userStats.map((stat, i) => (
            <StatsCard key={i} {...stat} />
          ))}
        </div>

        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Recent Challenges
        </h2>

        {recent_challenges.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <p className="text-center text-gray-600 dark:text-gray-400 py-8">
              No challenges yet. Purchase a program to start your trading journey!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {recent_challenges.map((challenge) => (
              <div key={challenge.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {challenge.program_name}
                  </h3>
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(challenge.status)}`}>
                    {challenge.status.toUpperCase()}
                  </span>
                </div>

                <div className="mb-4">
                  <div className="flex justify-between mb-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Progress</span>
                    <span className="text-sm font-semibold text-gray-900 dark:text-white">
                      {Math.round(calculateProgress(challenge))}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-purple-600 to-purple-800 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${calculateProgress(challenge)}%` }}
                    ></div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Current Balance</p>
                    <p className="text-lg font-semibold text-blue-600 dark:text-blue-400">
                      ${challenge.current_balance.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Profit/Loss</p>
                    <p className={`text-lg font-semibold ${challenge.profit >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                      ${challenge.profit.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Phase</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                      {challenge.phase || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Started</p>
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">
                      {challenge.created_at ? new Date(challenge.created_at).toLocaleDateString() : 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </UserLayout>
  );
}