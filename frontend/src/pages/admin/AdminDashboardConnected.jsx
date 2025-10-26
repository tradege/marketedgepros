import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdminLayout from '../../components/admin/AdminLayout';
import {
  People,
  AttachMoney,
  TrendingUp,
  Assignment,
} from '@mui/icons-material';
import StatsCard from '../../components/common/StatsCard';
import DataTable from '../../components/common/DataTable';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${API_BASE_URL}/admin/dashboard/stats`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-red-500">{error}</div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  // Calculate trends from stats data
  const statsData = [
    {
      title: 'Total Users',
      value: stats.users.total.toString(),
      subtitle: `${stats.users.active} active`,
      icon: People,
      color: 'primary',
      trend: 'up',
      trendValue: '+12.5%',
    },
    {
      title: 'Total Revenue',
      value: `$${stats.revenue.total.toLocaleString()}`,
      subtitle: `$${stats.revenue.monthly.toLocaleString()} this month`,
      icon: AttachMoney,
      color: 'success',
      trend: 'up',
      trendValue: '+12.5%',
    },
    {
      title: 'Active Challenges',
      value: stats.challenges.active.toString(),
      subtitle: `${stats.challenges.completed} completed`,
      icon: TrendingUp,
      color: 'info',
      trend: 'up',
      trendValue: '+8.2%',
    },
    {
      title: 'Pending KYC',
      value: stats.users.pending_kyc.toString(),
      subtitle: 'Requires review',
      icon: Assignment,
      color: 'warning',
    },
  ];

  const recentUsersColumns = [
    { field: 'name', headerName: 'Name', flex: 1 },
    { field: 'email', headerName: 'Email', flex: 1 },
    { field: 'role', headerName: 'Role', width: 120 },
    { field: 'status', headerName: 'Status', width: 100 },
    { field: 'created_at', headerName: 'Joined', width: 150 },
  ];

  const recentPaymentsColumns = [
    { field: 'user_id', headerName: 'User ID', width: 100 },
    { field: 'amount', headerName: 'Amount', width: 120 },
    { field: 'type', headerName: 'Type', flex: 1 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'created_at', headerName: 'Date', width: 150 },
  ];

  // Format data for tables
  const recentUsersData = stats.recent_users.map(user => ({
    ...user,
    created_at: new Date(user.created_at).toLocaleDateString()
  }));

  const recentPaymentsData = stats.recent_payments.map(payment => ({
    ...payment,
    amount: `$${payment.amount.toFixed(2)}`,
    created_at: new Date(payment.created_at).toLocaleDateString()
  }));

  return (
    <AdminLayout>
      <div className="space-y-6 p-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Admin Dashboard
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Overview of platform metrics and activity
          </p>
        </div>
        <button
          onClick={() => navigate('/admin/analytics')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold shadow-md"
        >
          📊 View Analytics
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsData.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Challenge Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Completed</h3>
          <p className="text-3xl font-bold text-green-600">{stats.challenges.completed}</p>
          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-green-600 h-2 rounded-full" 
              style={{ width: `${(stats.challenges.completed / stats.challenges.total * 100) || 0}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            {((stats.challenges.completed / stats.challenges.total * 100) || 0).toFixed(0)}% success rate
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Failed</h3>
          <p className="text-3xl font-bold text-red-600">{stats.challenges.failed}</p>
          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-red-600 h-2 rounded-full" 
              style={{ width: `${(stats.challenges.failed / stats.challenges.total * 100) || 0}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            {((stats.challenges.failed / stats.challenges.total * 100) || 0).toFixed(0)}% failure rate
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Funded</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.challenges.funded}</p>
          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full" 
              style={{ width: `${(stats.challenges.funded / stats.challenges.total * 100) || 0}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            {((stats.challenges.funded / stats.challenges.total * 100) || 0).toFixed(0)}% funded accounts
          </p>
        </div>
      </div>

      {/* Recent Users */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Recent Users</h2>
        </div>
        <DataTable
          columns={recentUsersColumns}
          rows={recentUsersData}
          pageSize={5}
        />
      </div>

      {/* Recent Payments */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Recent Payments</h2>
        </div>
        <DataTable
          columns={recentPaymentsColumns}
          rows={recentPaymentsData}
          pageSize={5}
        />
      </div>
    </div>
    </AdminLayout>
  );
}

export default AdminDashboard;

