import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

/**
 * Affiliate Dashboard Component
 * Shows commission statistics, progress, and earnings
 */
const AffiliateDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/affiliate/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch statistics');
      }

      const data = await response.json();
      setStats(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error: {error}</p>
        </div>
      </div>
    );
  }

  const progressPercentage = (stats.threshold_progress / stats.threshold_target) * 100;
  const canWithdraw = stats.can_withdraw && stats.commission_balance > 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Affiliate Dashboard</h1>
        <p className="mt-2 text-gray-600">Track your commissions and earnings</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Paid Customers Progress */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-500">Paying Customers</h3>
            <span className="text-2xl">👥</span>
          </div>
          <div className="mb-2">
            <p className="text-3xl font-bold text-gray-900">
              {stats.paid_customers_count} / {stats.threshold_target}
            </p>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500">
            {stats.paid_customers_count >= stats.threshold_target
              ? '✅ Threshold reached!'
              : `${stats.threshold_target - stats.paid_customers_count} more to unlock commissions`}
          </p>
        </div>

        {/* Pending Commission */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-500">Pending Commission</h3>
            <span className="text-2xl">⏳</span>
          </div>
          <p className="text-3xl font-bold text-yellow-600">
            ${stats.pending_commission.toFixed(2)}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            {stats.paid_customers_count < stats.threshold_target
              ? 'Locked until 10 customers'
              : 'Released to balance'}
          </p>
        </div>

        {/* Available Balance */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-500">Available Balance</h3>
            <span className="text-2xl">💰</span>
          </div>
          <p className="text-3xl font-bold text-green-600">
            ${stats.commission_balance.toFixed(2)}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            {canWithdraw ? 'Ready to withdraw' : 'Not yet eligible'}
          </p>
        </div>

        {/* Total Earned */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-500">Total Earned</h3>
            <span className="text-2xl">📈</span>
          </div>
          <p className="text-3xl font-bold text-blue-600">
            ${stats.total_earned.toFixed(2)}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Commission rate: {stats.commission_rate}%
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 mb-8">
        <Link
          to="/affiliate/withdraw"
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            canWithdraw
              ? 'bg-green-600 text-white hover:bg-green-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          onClick={(e) => !canWithdraw && e.preventDefault()}
        >
          Request Withdrawal
        </Link>
        <Link
          to="/affiliate/payment-method"
          className="px-6 py-3 rounded-lg font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors"
        >
          Payment Settings
        </Link>
        <Link
          to="/affiliate/customers"
          className="px-6 py-3 rounded-lg font-medium bg-gray-600 text-white hover:bg-gray-700 transition-colors"
        >
          My Customers
        </Link>
      </div>

      {/* Recent Commissions Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Recent Commissions</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats.commissions && stats.commissions.length > 0 ? (
                stats.commissions.slice(0, 10).map((commission) => (
                  <tr key={commission.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {commission.customer_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {commission.customer_email}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        ${commission.amount.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          commission.status === 'paid'
                            ? 'bg-green-100 text-green-800'
                            : commission.status === 'released'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {commission.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(commission.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                    No commissions yet. Start referring customers to earn!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {stats.commissions && stats.commissions.length > 10 && (
          <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
            <Link
              to="/affiliate/commissions"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              View all commissions →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default AffiliateDashboard;

