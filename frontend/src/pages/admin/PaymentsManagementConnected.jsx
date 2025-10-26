import { useState, useEffect } from 'react';
import AdminLayout from '../../components/admin/AdminLayout';
import { DollarSign, TrendingUp, CheckCircle, Clock } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

function PaymentsManagement() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    pages: 0
  });
  const [filters, setFilters] = useState({
    status: '',
    type: ''
  });

  useEffect(() => {
    fetchPayments();
  }, [pagination.page, filters]);

  const fetchPayments = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      const params = new URLSearchParams({
        page: pagination.page.toString(),
        per_page: pagination.per_page.toString(),
      });
      
      if (filters.status) params.append('status', filters.status);

      const response = await axios.get(
        `${API_BASE_URL}/admin/payments?${params.toString()}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setPayments(response.data.payments);
      setPagination(prev => ({
        ...prev,
        total: response.data.pagination.total,
        pages: response.data.pagination.pages
      }));
      setError(null);
    } catch (err) {
      setError('Failed to load payments');
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
  };

  // Calculate stats
  const stats = {
    totalRevenue: payments.reduce((sum, p) => p.status === 'completed' ? sum + p.amount : sum, 0),
    pendingPayouts: payments.reduce((sum, p) => p.status === 'pending' && p.payment_type === 'withdrawal' ? sum + p.amount : sum, 0),
    completedPayouts: payments.reduce((sum, p) => p.status === 'completed' && p.payment_type === 'withdrawal' ? sum + p.amount : sum, 0),
    pendingCount: payments.filter(p => p.status === 'pending').length,
  };

  const getStatusBadgeColor = (status) => {
    const colors = {
      completed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      failed: 'bg-red-100 text-red-800',
      refunded: 'bg-slate-700/50 text-gray-100'
    };
    return colors[status] || 'bg-slate-700/50 text-gray-100';
  };

  const getTypeBadgeColor = (type) => {
    const colors = {
      challenge_purchase: 'bg-blue-100 text-blue-800',
      withdrawal: 'bg-green-100 text-green-800',
      refund: 'bg-red-100 text-red-800'
    };
    return colors[type] || 'bg-slate-700/50 text-gray-100';
  };

  if (loading && payments.length === 0) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white dark:text-white">
          Payments Management
        </h1>
        <p className="mt-2 text-sm text-gray-300 dark:text-gray-400">
          Track and manage all payments and payouts
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 dark:text-green-400">Total Revenue</p>
              <p className="text-2xl font-bold text-green-900 dark:text-green-100">
                ${stats.totalRevenue.toLocaleString()}
              </p>
              <p className="text-xs text-green-600 dark:text-green-400 mt-1">+12.5% this month</p>
            </div>
            <DollarSign className="w-12 h-12 text-green-600 dark:text-green-400" />
          </div>
        </div>

        <div className="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-600 dark:text-yellow-400">Pending Payouts</p>
              <p className="text-2xl font-bold text-yellow-900 dark:text-yellow-100">
                ${stats.pendingPayouts.toLocaleString()}
              </p>
              <p className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">{stats.pendingCount} requests</p>
            </div>
            <Clock className="w-12 h-12 text-yellow-600 dark:text-yellow-400" />
          </div>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 dark:text-blue-400">Completed Payouts</p>
              <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                ${stats.completedPayouts.toLocaleString()}
              </p>
              <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">This month</p>
            </div>
            <CheckCircle className="w-12 h-12 text-blue-600 dark:text-blue-400" />
          </div>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-600 dark:text-purple-400">Average Payout</p>
              <p className="text-2xl font-bold text-purple-900 dark:text-purple-100">
                ${payments.length > 0 ? (stats.totalRevenue / payments.length).toFixed(0) : 0}
              </p>
              <p className="text-xs text-purple-600 dark:text-purple-400 mt-1">Per trader</p>
            </div>
            <TrendingUp className="w-12 h-12 text-purple-600 dark:text-purple-400" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-slate-800/50 dark:bg-gray-800 p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Status</label>
            <select
              className="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            >
              <option value="">All Status</option>
              <option value="completed">Completed</option>
              <option value="pending">Pending</option>
              <option value="failed">Failed</option>
              <option value="refunded">Refunded</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Type</label>
            <select
              className="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              value={filters.type}
              onChange={(e) => setFilters({ ...filters, type: e.target.value })}
            >
              <option value="">All Types</option>
              <option value="challenge_purchase">Purchase</option>
              <option value="withdrawal">Payout</option>
              <option value="refund">Refund</option>
            </select>
          </div>
        </div>
      </div>

      {/* Payments Table */}
      <div className="bg-slate-800/50 dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-900 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Transaction ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  User ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Method
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 dark:text-gray-300 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-slate-800/50 dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {payments.map((payment) => (
                <tr key={payment.id} className="hover:bg-slate-900 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-white dark:text-white">
                    {payment.transaction_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 dark:text-gray-400">
                    #{payment.user_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-white dark:text-white">
                    ${payment.amount.toFixed(2)} {payment.currency}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getTypeBadgeColor(payment.payment_type)}`}>
                      {payment.payment_type ? payment.payment_type.replace('_', ' ') : 'N/A'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadgeColor(payment.status)}`}>
                      {payment.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 dark:text-gray-400">
                    {payment.payment_method || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 dark:text-gray-400">
                    {new Date(payment.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-slate-900 dark:bg-gray-700 px-6 py-3 flex items-center justify-between">
          <div className="text-sm text-gray-200 dark:text-gray-300">
            Showing {((pagination.page - 1) * pagination.per_page) + 1} to {Math.min(pagination.page * pagination.per_page, pagination.total)} of {pagination.total} payments
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={pagination.page === 1}
              className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="px-3 py-1">
              Page {pagination.page} of {pagination.pages}
            </span>
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={pagination.page >= pagination.pages}
              className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </AdminLayout>
    </div>
  );
}

export default PaymentsManagement;

