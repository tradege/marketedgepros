import React, { useState, useEffect } from 'react';

/**
 * Admin Withdrawal Panel Component
 * Allows Super Master to manage withdrawal requests
 */
const AdminWithdrawalPanel = () => {
  const [activeTab, setActiveTab] = useState('pending');
  const [withdrawals, setWithdrawals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState(null);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [selectedWithdrawal, setSelectedWithdrawal] = useState(null);
  const [rejectReason, setRejectReason] = useState('');

  useEffect(() => {
    fetchWithdrawals();
  }, [activeTab]);

  const fetchWithdrawals = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/admin/withdrawals/${activeTab}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setWithdrawals(data.withdrawals || []);
      }
    } catch (err) {
      console.error('Error fetching withdrawals:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (withdrawalId) => {
    if (!confirm('Are you sure you want to approve this withdrawal?')) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/withdrawals/${withdrawalId}/approve`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Withdrawal approved successfully!' });
        fetchWithdrawals();
      } else {
        const data = await response.json();
        setMessage({ type: 'error', text: data.error || 'Failed to approve withdrawal' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'An error occurred' });
    }
  };

  const handleMarkPaid = async (withdrawalId) => {
    if (!confirm('Confirm that you have sent the payment to the user?')) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/withdrawals/${withdrawalId}/mark-paid`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Withdrawal marked as paid!' });
        fetchWithdrawals();
      } else {
        const data = await response.json();
        setMessage({ type: 'error', text: data.error || 'Failed to mark as paid' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'An error occurred' });
    }
  };

  const handleReject = async () => {
    if (!rejectReason.trim()) {
      alert('Please provide a reason for rejection');
      return;
    }

    try {
      const response = await fetch(`/api/admin/withdrawals/${selectedWithdrawal.id}/reject`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ reason: rejectReason }),
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Withdrawal rejected' });
        setShowRejectModal(false);
        setRejectReason('');
        setSelectedWithdrawal(null);
        fetchWithdrawals();
      } else {
        const data = await response.json();
        setMessage({ type: 'error', text: data.error || 'Failed to reject withdrawal' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'An error occurred' });
    }
  };

  const openRejectModal = (withdrawal) => {
    setSelectedWithdrawal(withdrawal);
    setShowRejectModal(true);
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

  const formatPaymentDetails = (details) => {
    if (!details) return 'N/A';
    
    if (details.method_type === 'bank') {
      return `${details.bank_name} - ${details.account_holder_name}`;
    } else if (details.method_type === 'paypal') {
      return details.paypal_email;
    } else if (details.method_type === 'crypto') {
      return `${details.crypto_network} - ${details.crypto_address}`;
    } else if (details.method_type === 'wise') {
      return details.wise_email;
    }
    return 'N/A';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Withdrawal Management</h1>
        <p className="mt-2 text-gray-600">Review and process affiliate withdrawal requests</p>
      </div>

      {/* Message */}
      {message && (
        <div
          className={`rounded-lg p-4 mb-6 ${
            message.type === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}
        >
          <div className="flex justify-between items-center">
            <span>{message.text}</span>
            <button onClick={() => setMessage(null)} className="text-lg font-bold">×</button>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {[
              { key: 'pending', label: 'Pending', count: withdrawals.length },
              { key: 'approved', label: 'Approved', count: 0 },
              { key: 'paid', label: 'Paid', count: 0 },
              { key: 'rejected', label: 'Rejected', count: 0 },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.key
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
                {activeTab === tab.key && withdrawals.length > 0 && (
                  <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-full">
                    {withdrawals.length}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Withdrawals Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : withdrawals.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No {activeTab} withdrawals</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Payment Method
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Details
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Requested
                  </th>
                  {activeTab === 'pending' && (
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  )}
                  {activeTab === 'approved' && (
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  )}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {withdrawals.map((withdrawal) => (
                  <tr key={withdrawal.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {withdrawal.user_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {withdrawal.user_email}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-bold text-gray-900">
                        ${withdrawal.amount.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {withdrawal.method_type.charAt(0).toUpperCase() + withdrawal.method_type.slice(1)}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900 max-w-xs truncate">
                        {formatPaymentDetails(withdrawal.payment_details)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(withdrawal.requested_at).toLocaleString()}
                    </td>
                    {activeTab === 'pending' && (
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleApprove(withdrawal.id)}
                          className="text-green-600 hover:text-green-900 mr-4"
                        >
                          ✓ Approve
                        </button>
                        <button
                          onClick={() => openRejectModal(withdrawal)}
                          className="text-red-600 hover:text-red-900"
                        >
                          ✗ Reject
                        </button>
                      </td>
                    )}
                    {activeTab === 'approved' && (
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleMarkPaid(withdrawal.id)}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                        >
                          Mark as Paid
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Reject Withdrawal</h3>
            <p className="text-gray-600 mb-4">
              Please provide a reason for rejecting this withdrawal request:
            </p>
            <textarea
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              rows="4"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter rejection reason..."
            ></textarea>
            <div className="flex gap-4 mt-6">
              <button
                onClick={handleReject}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Reject
              </button>
              <button
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectReason('');
                  setSelectedWithdrawal(null);
                }}
                className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminWithdrawalPanel;

