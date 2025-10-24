import { useEffect, useState } from 'react';
import { DollarSign, Clock, CheckCircle, XCircle, Plus } from 'lucide-react';
import TraderLayout from '../../components/trader/TraderLayout';
import api from '../../services/api';

export default function Withdrawals() {
  const [withdrawals, setWithdrawals] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [availableBalance, setAvailableBalance] = useState(5450);
  const [formData, setFormData] = useState({
    amount: '',
    method: 'bank_transfer',
    accountDetails: '',
  });

  useEffect(() => {
    loadWithdrawals();
  }, []);

  const loadWithdrawals = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/traders/withdrawals');
      setWithdrawals(response.data.withdrawals || []);
    } catch (error) {
      // Mock data for development
      setWithdrawals([
        {
          id: 1,
          amount: 2500,
          method: 'bank_transfer',
          status: 'completed',
          requested_date: '2024-10-10T10:30:00Z',
          processed_date: '2024-10-12T14:20:00Z',
          transaction_id: 'WD-2024-001',
        },
        {
          id: 2,
          amount: 1800,
          method: 'paypal',
          status: 'pending',
          requested_date: '2024-10-15T09:15:00Z',
          processed_date: null,
          transaction_id: 'WD-2024-002',
        },
        {
          id: 3,
          amount: 3200,
          method: 'bank_transfer',
          status: 'processing',
          requested_date: '2024-10-17T11:45:00Z',
          processed_date: null,
          transaction_id: 'WD-2024-003',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const amount = parseFloat(formData.amount);
    if (amount <= 0 || amount > availableBalance) {
      alert('Invalid withdrawal amount');
      return;
    }

    try {
      await api.post('/traders/withdrawals', formData);
      loadWithdrawals();
      setShowModal(false);
      setFormData({ amount: '', method: 'bank_transfer', accountDetails: '' });
      alert('Withdrawal request submitted successfully');
    } catch (error) {
      alert('Failed to submit withdrawal request. Please try again.');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'processing':
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case 'rejected':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return null;
    }
  };

  const stats = {
    totalWithdrawn: withdrawals.filter(w => w.status === 'completed').reduce((sum, w) => sum + w.amount, 0),
    pendingWithdrawals: withdrawals.filter(w => w.status === 'pending' || w.status === 'processing').reduce((sum, w) => sum + w.amount, 0),
    completedCount: withdrawals.filter(w => w.status === 'completed').length,
  };

  if (isLoading) {
    return (
      <TraderLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="text-gray-600 mt-4">Loading withdrawals...</p>
          </div>
        </div>
      </TraderLayout>
    );
  }

  return (
    <TraderLayout>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Withdrawals</h1>
                <p className="text-gray-600 mt-2">Request and track your payouts</p>
              </div>
              <button
                onClick={() => setShowModal(true)}
                className="btn btn-primary flex items-center gap-2"
              >
                <Plus className="w-5 h-5" />
                New Withdrawal
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Available Balance</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    ${availableBalance.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Withdrawn</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    ${stats.totalWithdrawn.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    ${stats.pendingWithdrawals.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-yellow-600" />
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Completed</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stats.completedCount}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>
          </div>

          {/* Withdrawals List */}
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Transaction ID
                    </th>
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
                      Requested Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Processed Date
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {withdrawals.map((withdrawal) => (
                    <tr key={withdrawal.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {withdrawal.transaction_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                        ${withdrawal.amount.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                        {withdrawal.method.replace('_', ' ')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(withdrawal.status)}
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(withdrawal.status)}`}>
                            {withdrawal.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {new Date(withdrawal.requested_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {withdrawal.processed_date 
                          ? new Date(withdrawal.processed_date).toLocaleDateString()
                          : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {withdrawals.length === 0 && (
              <div className="text-center py-12">
                <DollarSign className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">No withdrawal requests yet</p>
                <button
                  onClick={() => setShowModal(true)}
                  className="btn btn-primary"
                >
                  Request Your First Withdrawal
                </button>
              </div>
            )}
          </div>

          {/* Info Box */}
          <div className="mt-8 card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-bold text-blue-900 mb-2">Withdrawal Information</h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>• Minimum withdrawal amount: $100</li>
              <li>• Processing time: 1-3 business days</li>
              <li>• Withdrawals are processed on weekdays only</li>
              <li>• You can only withdraw profits from funded accounts</li>
              <li>• Bank transfer fees may apply depending on your bank</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Withdrawal Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">New Withdrawal Request</h2>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Available Balance
                </label>
                <div className="text-3xl font-bold text-green-600">
                  ${availableBalance.toLocaleString()}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Withdrawal Amount ($) *
                </label>
                <input
                  type="number"
                  required
                  min="100"
                  max={availableBalance}
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  className="input w-full"
                  placeholder="Enter amount"
                />
                <p className="text-xs text-gray-600 mt-1">
                  Minimum: $100 | Maximum: ${availableBalance.toLocaleString()}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Withdrawal Method *
                </label>
                <select
                  required
                  value={formData.method}
                  onChange={(e) => setFormData({ ...formData, method: e.target.value })}
                  className="input w-full"
                >
                  <option value="bank_transfer">Bank Transfer</option>
                  <option value="paypal">PayPal</option>
                  <option value="crypto">Cryptocurrency</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Account Details *
                </label>
                <textarea
                  required
                  value={formData.accountDetails}
                  onChange={(e) => setFormData({ ...formData, accountDetails: e.target.value })}
                  className="input w-full"
                  rows="4"
                  placeholder="Enter your account details (bank account number, PayPal email, crypto wallet address, etc.)"
                />
              </div>

              <div className="flex gap-4 pt-4">
                <button type="submit" className="btn btn-primary flex-1">
                  Submit Request
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setFormData({ amount: '', method: 'bank_transfer', accountDetails: '' });
                  }}
                  className="btn btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </TraderLayout>
  );
}

