import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

/**
 * Withdrawal Request Form Component
 * Allows affiliates to request commission withdrawals
 */
const WithdrawalRequestForm = () => {
  const [stats, setStats] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState(null);
  const [withdrawalHistory, setWithdrawalHistory] = useState([]);
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = {
        'Authorization': `Bearer ${token}`,
      };

      // Fetch stats
      const statsRes = await fetch('/api/affiliate/stats', { headers });
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }

      // Fetch eligibility
      const eligRes = await fetch('/api/withdrawal/eligibility', { headers });
      if (eligRes.ok) {
        const eligData = await eligRes.json();
        setEligibility(eligData);
      }

      // Fetch payment method
      const pmRes = await fetch('/api/payment-method', { headers });
      if (pmRes.ok) {
        const pmData = await pmRes.json();
        setPaymentMethod(pmData);
      }

      // Fetch withdrawal history
      const historyRes = await fetch('/api/withdrawal/history', { headers });
      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setWithdrawalHistory(historyData.withdrawals || []);
      }

      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);

    try {
      const response = await fetch('/api/withdrawal/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ amount: parseFloat(amount) }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: 'Withdrawal request submitted successfully!' });
        setAmount('');
        // Refresh data
        fetchData();
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to submit withdrawal request' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'An error occurred. Please try again.' });
    } finally {
      setSubmitting(false);
    }
  };

  const getStatusBadge = (status) => {
    const styles = {
      pending: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-blue-100 text-blue-800',
      paid: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return styles[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const canWithdraw = eligibility?.can_withdraw && stats?.commission_balance > 0 && paymentMethod;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Request Withdrawal</h1>
        <p className="mt-2 text-gray-600">Withdraw your commission earnings</p>
      </div>

      {/* Balance Card */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-8 mb-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-100 text-sm mb-1">Available Balance</p>
            <p className="text-5xl font-bold">${stats?.commission_balance.toFixed(2) || '0.00'}</p>
          </div>
          <div className="text-6xl opacity-20">💰</div>
        </div>
      </div>

      {/* Eligibility Status */}
      {!canWithdraw && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
          <div className="flex items-start">
            <span className="text-3xl mr-4">⚠️</span>
            <div className="flex-1">
              <h3 className="font-bold text-yellow-900 mb-2">Not Eligible to Withdraw</h3>
              <p className="text-yellow-800 mb-4">{eligibility?.reason}</p>
              
              {!paymentMethod && (
                <Link
                  to="/affiliate/payment-method"
                  className="inline-block px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
                >
                  Set Up Payment Method
                </Link>
              )}
              
              {eligibility?.days_remaining > 0 && (
                <p className="text-sm text-yellow-700 mt-2">
                  You can withdraw again in {eligibility.days_remaining} days
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Message */}
      {message && (
        <div
          className={`rounded-lg p-4 mb-6 ${
            message.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Withdrawal Form */}
      {canWithdraw && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Request New Withdrawal</h2>
          
          {/* Payment Method Info */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Payment Method</p>
                <p className="font-medium text-gray-900">
                  {paymentMethod?.method_type.charAt(0).toUpperCase() + paymentMethod?.method_type.slice(1)}
                  {paymentMethod?.method_type === 'bank' && ` - ${paymentMethod.bank_name}`}
                  {paymentMethod?.method_type === 'paypal' && ` - ${paymentMethod.paypal_email}`}
                  {paymentMethod?.method_type === 'crypto' && ` - ${paymentMethod.crypto_network}`}
                </p>
              </div>
              <Link
                to="/affiliate/payment-method"
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Change
              </Link>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Withdrawal Amount (USD)
              </label>
              <div className="relative">
                <span className="absolute left-4 top-3 text-gray-500 text-lg">$</span>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="1"
                  max={stats?.commission_balance}
                  step="0.01"
                  required
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                  placeholder="0.00"
                />
              </div>
              <div className="flex justify-between mt-2">
                <p className="text-sm text-gray-500">
                  Available: ${stats?.commission_balance.toFixed(2)}
                </p>
                <button
                  type="button"
                  onClick={() => setAmount(stats?.commission_balance.toString())}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Withdraw All
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting || !amount || parseFloat(amount) <= 0}
              className="w-full px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {submitting ? 'Submitting...' : 'Submit Withdrawal Request'}
            </button>
          </form>
        </div>
      )}

      {/* Withdrawal History */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Withdrawal History</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Method
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Requested
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Completed
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {withdrawalHistory.length > 0 ? (
                withdrawalHistory.map((withdrawal) => (
                  <tr key={withdrawal.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        ${withdrawal.amount.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {withdrawal.method_type.charAt(0).toUpperCase() + withdrawal.method_type.slice(1)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadge(
                          withdrawal.status
                        )}`}
                      >
                        {withdrawal.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(withdrawal.requested_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {withdrawal.paid_at
                        ? new Date(withdrawal.paid_at).toLocaleDateString()
                        : '-'}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                    No withdrawal history yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default WithdrawalRequestForm;

